from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Request, Form, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app.domain.auth.schemas import UserCreate, UserResponse, TokenResponse, UserPreferencesCreate, UserPreferencesResponse
from app.domain.auth.schemas import UserSubscriptionCreate, UserSubscriptionUpdate, UserSubscriptionResponse, SubscriptionStatusEnum
from app.domain.auth.service import AuthService
from app.core.dependencies import get_auth_service, get_current_user_id
from app.infrastructure.database import get_db
from app.core.config import get_settings
import httpx
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pydantic import ValidationError
from sqlalchemy.orm import Session
import os

settings = get_settings()
router = APIRouter()
logger = logging.getLogger("auth_routes")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    """
    Rota para registrar um novo usuário.
    """
    # Verificar se o usuário já existe
    existing_user = auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Usuário já registrado",
                "code": "USER_EXISTS"
            }
        )

    # Registrar o usuário
    new_user = auth_service.register_user(user_data)

    return {
        "message": "Usuário cadastrado com sucesso",
        "user_id": str(new_user.id)
    }


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate and log in a user.
    """
    try:
        # Verificar se existem credenciais processadas pelo middleware no state
        credentials = getattr(request.state, "credentials", None)

        # Se o middleware processou credenciais JSON, usá-las em vez de form_data
        username = credentials.get(
            "username", form_data.username) if credentials else form_data.username
        password = credentials.get(
            "password", form_data.password) if credentials else form_data.password

        # Prosseguir com a autenticação
        user = auth_service.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access and refresh tokens
        access_token = auth_service.create_access_token(data={"sub": user.id})
        refresh_token = auth_service.create_refresh_token(
            data={"sub": user.id})

        # Set tokens as HttpOnly cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",  # mudar para 'strict' em produção
            max_age=60 * 15,  # 15 minutes
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",  # mudar para 'strict' em produção
            max_age=60 * 60 * 24 * 7,  # 7 days
        )

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user": user}
    except Exception as e:
        logger.error(f"Erro durante o login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro durante a autenticação",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout")
def logout(response: Response):
    """
    Log out a user by clearing cookies.
    """
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
def get_current_user(auth_service: AuthService = Depends(get_auth_service), user_id: str = Depends(get_current_user_id)):
    """
    Get the current authenticated user.
    """
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("/preferences", response_model=UserPreferencesResponse)
async def create_user_preferences(
    preferences: UserPreferencesCreate,
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Create or update user preferences from onboarding.
    """
    try:
        # Check if user exists
        user = auth_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create or update preferences
        preferences_db = auth_service.create_user_preferences(
            user_id, preferences)

        # Atualizar explicitamente o status de onboarding do usuário se necessário
        # A função update_onboarding_completed agora atualiza tanto a tabela de preferências quanto a tabela de usuários
        if preferences.onboarding_completed:
            auth_service.update_onboarding_completed(user_id, True)

        # Forward preferences to MS-Study service
        if settings.ms_study_url:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    # Include user information with preferences
                    payload = {
                        "user_id": user_id,
                        "name": user.name,
                        "email": user.email,
                        "objectives": preferences.objectives,
                        "bible_experience_level": preferences.bible_experience_level,
                        "content_preferences": preferences.content_preferences,
                        "preferred_time": preferences.preferred_time,
                        "onboarding_completed": preferences.onboarding_completed
                    }

                    # Enviar preferências para o MS-Study
                    logger.info(
                        f"Sending preferences to MS-Study for user {user_id}")
                    response = await client.post(
                        f"{settings.ms_study_url}/api/v1/study/preferences",
                        json=payload,
                        headers={
                            "Authorization": f"Bearer {settings.service_api_key}"}
                    )

                    if response.status_code in (200, 201):
                        logger.info(
                            f"Successfully sent preferences to MS-Study for user {user_id}")

                        # Se o onboarding estiver completo, gerar plano de estudo
                        if preferences.onboarding_completed:
                            logger.info(
                                f"Initiating study plan generation for user {user_id}")
                            plan_response = await client.post(
                                f"{settings.ms_study_url}/api/v1/study/init-plan",
                                json=payload,
                                headers={
                                    "Authorization": f"Bearer {settings.service_api_key}"}
                            )

                            if plan_response.status_code == 201:
                                logger.info(
                                    f"Successfully generated study plan for user {user_id}")
                            else:
                                logger.error(
                                    f"Failed to generate study plan: {plan_response.status_code} - {plan_response.text}")
                    else:
                        logger.error(
                            f"Failed to send preferences to MS-Study: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Error communicating with MS-Study: {str(e)}")
                # Não falhar a requisição se a comunicação com MS-Study falhar
                # Apenas logar o erro e retornar as preferências salvas

        return preferences_db
    except Exception as e:
        logger.error(f"Error processing user preferences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing user preferences: {str(e)}"
        )


@router.get("/preferences", response_model=UserPreferencesResponse)
def get_user_preferences(
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Get user preferences.
    """
    preferences = auth_service.get_user_preferences(user_id)
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found"
        )
    return preferences


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Rota para verificar se o serviço está funcionando.
    """
    return {"status": "healthy", "service": "ms-auth"}


@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Refresh the access token using a valid refresh token.
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Verify refresh token and get user_id
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create new tokens
        new_access_token = auth_service.create_access_token(
            data={"sub": user_id})
        new_refresh_token = auth_service.create_refresh_token(
            data={"sub": user_id})

        # Set new tokens as cookies
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=60 * 15,  # 15 minutes
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=60 * 60 * 24 * 7,  # 7 days
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/verify-token")
def verify_token(
    token_data: dict,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Verify if a token is valid.
    """
    try:
        token = token_data.get("token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token not provided"
            )

        payload = auth_service.decode_token(token)
        return {"valid": True, "payload": payload}
    except Exception as e:
        return {"valid": False, "error": str(e)}


# === Endpoints para gerenciamento de assinaturas ===

@router.get("/subscription", response_model=UserSubscriptionResponse)
async def get_user_subscription(
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Obtém os detalhes da assinatura atual do usuário.
    """
    subscription = auth_service.get_user_subscription(user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return subscription


@router.post("/subscription", response_model=UserSubscriptionResponse)
async def create_or_update_subscription(
    subscription_data: UserSubscriptionCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Cria ou atualiza a assinatura de um usuário (endpoint administrativo ou para webhooks de pagamento).
    """
    # Verificar se o usuário existe
    user = auth_service.get_user_by_id(subscription_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    subscription = auth_service.create_subscription(subscription_data)
    return subscription


@router.put("/subscription", response_model=UserSubscriptionResponse)
async def update_current_user_subscription(
    subscription_data: UserSubscriptionUpdate,
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Atualiza a assinatura do usuário autenticado.
    """
    subscription = auth_service.update_subscription(user_id, subscription_data)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return subscription


@router.post("/subscription/cancel", response_model=UserSubscriptionResponse)
async def cancel_subscription(
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Cancela a assinatura do usuário autenticado.
    """
    subscription = auth_service.cancel_subscription(user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return subscription


@router.get("/subscription/status")
async def get_subscription_status(
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Retorna informações detalhadas sobre o status da assinatura do usuário.
    """
    status_info = auth_service.check_subscription_status(user_id)
    return status_info


@router.post("/subscription/webhook")
async def subscription_webhook(
    payload: Dict[str, Any],
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Endpoint para receber webhooks de gateways de pagamento (Stripe/Hotmart).
    """
    try:
        logger.info(f"Recebido webhook de pagamento: {payload}")

        # Exemplo de processamento para Stripe
        if "type" in payload and payload["type"].startswith("customer.subscription"):
            # Processar evento de assinatura Stripe
            if payload["type"] == "customer.subscription.created" or payload["type"] == "customer.subscription.updated":
                # Obter dados relevantes
                customer_id = payload.get("data", {}).get(
                    "object", {}).get("customer", "")
                subscription_id = payload.get("data", {}).get(
                    "object", {}).get("id", "")
                status = payload.get("data", {}).get(
                    "object", {}).get("status", "")

                # Mapear status do Stripe para nosso modelo
                status_mapping = {
                    "active": SubscriptionStatusEnum.ACTIVE,
                    "canceled": SubscriptionStatusEnum.CANCELLED,
                    "incomplete": SubscriptionStatusEnum.PENDING,
                    "incomplete_expired": SubscriptionStatusEnum.INACTIVE,
                    # Decisão de negócio manter ativo até expirar
                    "past_due": SubscriptionStatusEnum.ACTIVE,
                    "trialing": SubscriptionStatusEnum.ACTIVE,
                    "unpaid": SubscriptionStatusEnum.INACTIVE
                }

                # Encontrar o usuário pelo customer_id (armazenado no metadata)
                # Na implementação real, teríamos uma tabela ou campo para armazenar essa relação
                # Aqui é apenas um exemplo simplificado
                # Na implementação real, seria necessário buscar o user_id correspondente
                user_id = customer_id

                if user_id:
                    # Definir data de expiração (exemplo: 30 dias a partir de agora)
                    expiration_date = datetime.utcnow() + timedelta(days=30)

                    # Atualizar assinatura
                    subscription_data = UserSubscriptionUpdate(
                        subscription_type="premium",
                        status=status_mapping.get(
                            status, SubscriptionStatusEnum.INACTIVE),
                        payment_gateway="stripe",
                        expiration_date=expiration_date,
                        last_payment_date=datetime.utcnow()
                    )

                    auth_service.update_subscription(
                        user_id, subscription_data)
                    logger.info(
                        f"Assinatura atualizada com sucesso para o usuário {user_id}")
                else:
                    logger.error(
                        f"Não foi possível encontrar o usuário para o customer_id {customer_id}")

        # Exemplo para processamento Hotmart (simplificado)
        elif "event" in payload and payload["event"].startswith("PURCHASE"):
            # Processar evento de compra Hotmart
            if payload["event"] in ["PURCHASE_APPROVED", "PURCHASE_COMPLETE", "SUBSCRIPTION_RESTARTED"]:
                # Obter dados relevantes
                email = payload.get("data", {}).get(
                    "buyer", {}).get("email", "")
                product_id = payload.get("data", {}).get(
                    "product", {}).get("id", "")

                # Encontrar usuário pelo email
                if email:
                    user = auth_service.get_user_by_email(email)
                    if user:
                        # Definir data de expiração (exemplo: plano anual)
                        expiration_date = datetime.utcnow() + timedelta(days=365)

                        # Atualizar assinatura
                        subscription_data = UserSubscriptionUpdate(
                            subscription_type="premium",
                            status=SubscriptionStatusEnum.ACTIVE,
                            payment_gateway="hotmart",
                            expiration_date=expiration_date,
                            last_payment_date=datetime.utcnow()
                        )

                        auth_service.update_subscription(
                            user.id, subscription_data)
                        logger.info(
                            f"Assinatura Hotmart atualizada com sucesso para o usuário {user.id}")
                    else:
                        logger.error(
                            f"Usuário não encontrado para o email {email}")

            # Cancelamento Hotmart
            elif payload["event"] in ["SUBSCRIPTION_CANCELLED", "PURCHASE_CANCELED", "PURCHASE_REFUNDED"]:
                email = payload.get("data", {}).get(
                    "buyer", {}).get("email", "")
                if email:
                    user = auth_service.get_user_by_email(email)
                    if user:
                        auth_service.cancel_subscription(user.id)
                        logger.info(
                            f"Assinatura Hotmart cancelada para o usuário {user.id}")

        return {"status": "success", "message": "Webhook processed successfully"}

    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        # Não retornamos erro para o gateway de pagamento para evitar reenvios
        return {"status": "error", "message": str(e)}


@router.get("/verify-token")
def verify_token(user_id: str = Depends(get_current_user_id), auth_service: AuthService = Depends(get_auth_service)):
    """
    Verifica a validade do token atual e se ele precisa ser renovado.
    """
    # Se esta função foi executada, significa que o token é válido
    # pois passou pela dependência get_current_user_id

    # Verificar se o usuário existe
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verificar se o token está próximo da expiração (dentro de 5 minutos)
    # Como não conseguimos acessar o token diretamente (está em cookie HttpOnly),
    # apenas retornamos um flag para informar ao frontend

    # A lógica de verificação de expiração do token deve ser feita pelo cliente
    # com base no timestamp de expiração que ele recebeu ao fazer login

    return {
        "is_valid": True,
        "needsRefresh": False  # Este valor seria True se o token estivesse próximo da expiração
    }


@router.post("/forgot-password")
async def forgot_password(
    email_data: Dict[str, str] = Body(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Envia um e-mail com instruções para recuperação de senha.
    """
    email = email_data.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email não fornecido"
        )

    # Verificar se o usuário existe
    user = auth_service.get_user_by_email(email)
    if not user:
        # Não revelamos se o e-mail existe ou não por questões de segurança
        return {
            "message": "Se o e-mail estiver cadastrado, você receberá as instruções para recuperação de senha."
        }

    # Aqui você implementaria o envio real do e-mail
    # Como não temos um serviço de e-mail configurado, retornamos uma mensagem simulando o envio

    # Gerar um token para recuperação (validade de 1 hora)
    reset_token = auth_service.create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=timedelta(hours=1)
    )

    # Em um ambiente real, você enviaria o e-mail aqui com o link de recuperação
    reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}&email={user.email}"

    # Log para debug (em produção, essa informação estaria apenas no e-mail)
    logger.info(f"Link de recuperação de senha: {reset_link}")

    return {
        "message": "Se o e-mail estiver cadastrado, você receberá as instruções para recuperação de senha."
    }


@router.post("/reset-password")
async def reset_password(
    reset_data: Dict[str, str] = Body(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Redefine a senha do usuário usando o token enviado por e-mail.
    """
    token = reset_data.get("token")
    password = reset_data.get("password")
    email = reset_data.get("email")

    if not token or not password or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token, e-mail e nova senha são obrigatórios"
        )

    try:
        # Validar o token
        payload = auth_service.decode_token(token)
        user_id = payload.get("sub")
        token_email = payload.get("email")

        # Verificar se o e-mail no token corresponde ao e-mail fornecido
        if token_email != email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido ou expirado"
            )

        # Verificar se o usuário existe
        user = auth_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        # Atualizar a senha
        success = auth_service.update_password(user_id, password)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar a senha"
            )

        return {
            "message": "Senha atualizada com sucesso"
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado"
        )
    except Exception as e:
        logger.error(f"Erro na recuperação de senha: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar solicitação de recuperação de senha"
        )


@router.get("/user")
def get_current_user_compat(auth_service: AuthService = Depends(get_auth_service), user_id: str = Depends(get_current_user_id)):
    """
    Get the current authenticated user (compatibility endpoint).
    """
    logger.info(f"Recebida solicitação para obter dados do usuário {user_id}")

    # Reutiliza a mesma lógica do endpoint /me
    user = auth_service.get_user_by_id(user_id)
    if not user:
        logger.error(f"Usuário {user_id} não encontrado")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Log do tipo e valor do campo onboarding_completed
    logger.info(
        f"Tipo do campo onboarding_completed: {type(user.onboarding_completed)}")
    logger.info(
        f"Valor do campo onboarding_completed: {user.onboarding_completed}")

    # Garantir que o onboarding_completed seja um boolean
    onboarding_status = bool(
        user.onboarding_completed) if user.onboarding_completed is not None else False

    # Converter o modelo ORM para um dicionário
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "onboarding_completed": onboarding_status
    }

    # Log explícito do valor de onboarding_completed após a conversão
    logger.info(
        f"User {user_id} - onboarding_completed final: {user_dict['onboarding_completed']} (tipo: {type(user_dict['onboarding_completed'])})")

    return {"user": user_dict}
