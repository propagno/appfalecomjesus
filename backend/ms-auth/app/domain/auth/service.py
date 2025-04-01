from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union, List
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import logging
import uuid

from app.domain.auth.models import User, UserPreferences, UserSubscription, SubscriptionType, SubscriptionStatus
from app.domain.auth.schemas import UserCreate, UserInDB, TokenData, UserPreferencesCreate, UserSubscriptionCreate, UserSubscriptionUpdate
from app.core.config import get_settings
from app.infrastructure.database import get_db

logger = logging.getLogger("auth_service")

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_preferences(self, user_id: str):
        return self.db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()

    def create_user_preferences(self, user_id: str, preferences: UserPreferencesCreate) -> Optional[UserPreferences]:
        """
        Create or update user preferences.
        """
        try:
            # Check if preferences already exist for this user
            existing_prefs = self.get_user_preferences(user_id)
            user = self.get_user_by_id(user_id)

            if not user:
                logger.error(
                    f"User {user_id} not found when creating preferences")
                return None

            if existing_prefs:
                # Update existing preferences
                existing_prefs.objectives = preferences.objectives
                existing_prefs.bible_experience_level = preferences.bible_experience_level
                existing_prefs.content_preferences = preferences.content_preferences
                existing_prefs.preferred_time = preferences.preferred_time
                existing_prefs.onboarding_completed = preferences.onboarding_completed
                existing_prefs.updated_at = datetime.utcnow()
                db_preferences = existing_prefs
            else:
                # Create new preferences
                db_preferences = UserPreferences(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    objectives=preferences.objectives,
                    bible_experience_level=preferences.bible_experience_level,
                    content_preferences=preferences.content_preferences,
                    preferred_time=preferences.preferred_time,
                    onboarding_completed=preferences.onboarding_completed
                )
                self.db.add(db_preferences)

            # Update user's onboarding status if onboarding is completed
            if preferences.onboarding_completed:
                # Atualiza diretamente o campo onboarding_completed do usuário
                user.onboarding_completed = True
                user.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(db_preferences)

            # Refresh também o usuário
            if user:
                self.db.refresh(user)

            return db_preferences
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create/update user preferences: {str(e)}")
            raise

    def update_onboarding_completed(self, user_id: str, completed: bool = True):
        """
        Atualiza o status de onboarding tanto na tabela de preferências quanto na tabela de usuários.
        """
        db_preferences = self.get_user_preferences(user_id)
        user = self.get_user_by_id(user_id)

        if db_preferences:
            db_preferences.onboarding_completed = completed

        if user:
            user.onboarding_completed = completed

        self.db.commit()

        # Refresh apenas se as preferências existirem
        if db_preferences:
            self.db.refresh(db_preferences)

        # Refresh o usuário se existir
        if user:
            self.db.refresh(user)

        return db_preferences

    def register_user(self, user_data: UserCreate) -> Optional[User]:
        """
        Register a new user.
        """
        try:
            hashed_password = pwd_context.hash(user_data.password)
            user = User(
                id=str(uuid.uuid4()),
                email=user_data.email,
                name=user_data.name,
                hashed_password=hashed_password,
                is_active=True,
                is_admin=False
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            # Cria assinatura gratuita por padrão
            self.create_subscription(
                UserSubscriptionCreate(
                    user_id=user.id,
                    subscription_type=SubscriptionType.FREE.value,
                    status=SubscriptionStatus.ACTIVE.value
                )
            )

            return user
        except IntegrityError:
            self.db.rollback()
            logger.error(
                f"Failed to register user: {user_data.email} (already exists)")
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user.
        """
        user = self.get_user_by_email(email)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create an access token with optional custom expiration time.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create a refresh token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            days=settings.refresh_token_expire_days
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # === Métodos para gerenciamento de assinaturas ===

    def get_user_subscription(self, user_id: str) -> Optional[UserSubscription]:
        """
        Obtém a assinatura atual do usuário.
        """
        return self.db.query(UserSubscription).filter(UserSubscription.user_id == user_id).first()

    def create_subscription(self, subscription_data: UserSubscriptionCreate) -> UserSubscription:
        """
        Cria uma nova assinatura para o usuário.
        """
        try:
            # Verificar se já existe assinatura para este usuário
            existing_sub = self.get_user_subscription(
                subscription_data.user_id)

            if existing_sub:
                # Atualiza a assinatura existente
                existing_sub.subscription_type = getattr(
                    SubscriptionType, subscription_data.subscription_type.upper())
                existing_sub.status = getattr(
                    SubscriptionStatus, subscription_data.status.upper())
                existing_sub.payment_gateway = subscription_data.payment_gateway
                existing_sub.expiration_date = subscription_data.expiration_date
                existing_sub.updated_at = datetime.utcnow()

                if subscription_data.subscription_type.upper() == SubscriptionType.PREMIUM.name:
                    existing_sub.last_payment_date = datetime.utcnow()

                subscription = existing_sub
            else:
                # Cria uma nova assinatura
                subscription = UserSubscription(
                    id=str(uuid.uuid4()),
                    user_id=subscription_data.user_id,
                    subscription_type=getattr(
                        SubscriptionType, subscription_data.subscription_type.upper()),
                    status=getattr(SubscriptionStatus,
                                   subscription_data.status.upper()),
                    payment_gateway=subscription_data.payment_gateway,
                    expiration_date=subscription_data.expiration_date,
                    last_payment_date=datetime.utcnow() if subscription_data.subscription_type.upper(
                    ) == SubscriptionType.PREMIUM.name else None
                )
                self.db.add(subscription)

            self.db.commit()
            self.db.refresh(subscription)
            return subscription
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create subscription: {str(e)}")
            raise

    def update_subscription(self, user_id: str, subscription_data: UserSubscriptionUpdate) -> Optional[UserSubscription]:
        """
        Atualiza a assinatura de um usuário.
        """
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            logger.error(f"Subscription not found for user {user_id}")
            return None

        try:
            # Atualizar apenas os campos que foram fornecidos
            if subscription_data.subscription_type is not None:
                subscription.subscription_type = getattr(
                    SubscriptionType, subscription_data.subscription_type.upper())

            if subscription_data.status is not None:
                subscription.status = getattr(
                    SubscriptionStatus, subscription_data.status.upper())

            if subscription_data.payment_gateway is not None:
                subscription.payment_gateway = subscription_data.payment_gateway

            if subscription_data.expiration_date is not None:
                subscription.expiration_date = subscription_data.expiration_date

            if subscription_data.last_payment_date is not None:
                subscription.last_payment_date = subscription_data.last_payment_date

            subscription.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(subscription)
            return subscription
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update subscription: {str(e)}")
            raise

    def cancel_subscription(self, user_id: str) -> Optional[UserSubscription]:
        """
        Cancela a assinatura de um usuário.
        """
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            logger.error(f"Subscription not found for user {user_id}")
            return None

        try:
            subscription.status = SubscriptionStatus.CANCELLED
            subscription.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(subscription)
            return subscription
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to cancel subscription: {str(e)}")
            raise

    def check_subscription_status(self, user_id: str) -> Dict[str, Any]:
        """
        Verifica o status da assinatura de um usuário e retorna informações detalhadas.
        """
        subscription = self.get_user_subscription(user_id)

        if not subscription:
            # Se não existe assinatura, criar uma gratuita por padrão
            subscription = self.create_subscription(
                UserSubscriptionCreate(
                    user_id=user_id,
                    subscription_type=SubscriptionType.FREE.value,
                    status=SubscriptionStatus.ACTIVE.value
                )
            )

        # Verificar se a assinatura premium expirou
        if (subscription.subscription_type == SubscriptionType.PREMIUM and
            subscription.expiration_date and
                subscription.expiration_date < datetime.utcnow()):

            # Se expirou, regredir para assinatura gratuita
            subscription.subscription_type = SubscriptionType.FREE
            subscription.status = SubscriptionStatus.ACTIVE
            subscription.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(subscription)

        # Retornar informações detalhadas
        is_premium = subscription.subscription_type == SubscriptionType.PREMIUM
        is_active = subscription.status == SubscriptionStatus.ACTIVE

        return {
            "is_premium": is_premium,
            "is_active": is_active,
            "subscription_type": subscription.subscription_type.value,
            "status": subscription.status.value,
            "expiration_date": subscription.expiration_date,
            "days_remaining": (subscription.expiration_date - datetime.utcnow()).days if subscription.expiration_date else None,
            "last_payment_date": subscription.last_payment_date
        }

    def update_password(self, user_id: str, new_password: str) -> bool:
        """
        Update a user's password.
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                logger.error(
                    f"User {user_id} not found when updating password")
                return False

            hashed_password = self.get_password_hash(new_password)
            user.hashed_password = hashed_password
            user.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(user)
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(
                f"Failed to update password for user {user_id}: {str(e)}")
            return False

    def generate_password_reset_token(self, email: str) -> Optional[str]:
        """
        Generate a password reset token for the user.
        """
        user = self.get_user_by_email(email)
        if not user:
            logger.error(
                f"User with email {email} not found when generating reset token")
            return None

        # Create a token that expires in 1 hour
        token_data = {
            "sub": user.email,
            "type": "password_reset",
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

        # Generate the token
        token = jwt.encode(token_data, settings.secret_key,
                           algorithm=settings.algorithm)
        return token

    def verify_password_reset_token(self, token: str) -> Optional[str]:
        """
        Verify a password reset token and return the user's email if valid.
        """
        try:
            payload = jwt.decode(token, settings.secret_key,
                                 algorithms=[settings.algorithm])
            email = payload.get("sub")
            token_type = payload.get("type")

            if email is None or token_type != "password_reset":
                logger.error("Invalid token payload for password reset")
                return None

            return email
        except JWTError as e:
            logger.error(f"Invalid or expired password reset token: {str(e)}")
            return None
