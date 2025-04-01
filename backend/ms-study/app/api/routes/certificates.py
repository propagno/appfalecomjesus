from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.api.deps import get_current_active_user, get_current_user
from app.schemas.certificate import CertificateCreate, CertificateInDB, CertificateDetail, CertificateListResponse
from app.services.certificate_service import CertificateService

router = APIRouter()


@router.get("/", response_model=CertificateListResponse)
async def get_user_certificates(
    skip: int = Query(0, ge=0, description="Quantos itens pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Limite de itens por página"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista paginada dos certificados do usuário.

    Requer autenticação.
    """
    certificate_service = CertificateService(db)

    # Obter certificados do usuário
    certificates, total = await certificate_service.get_user_certificates(
        user_id=current_user["id"],
        skip=skip,
        limit=limit
    )

    # Calcular a página atual
    page = skip // limit + 1 if limit > 0 else 1

    return CertificateListResponse(
        items=certificates,
        total=total,
        page=page,
        page_size=limit
    )


@router.post("/", response_model=CertificateDetail, status_code=status.HTTP_201_CREATED)
async def create_certificate(
    certificate_data: CertificateCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo certificado de conclusão de plano de estudo.

    Requer autenticação.
    """
    certificate_service = CertificateService(db)

    # Verificar permissões (apenas o próprio usuário ou admin)
    if certificate_data.user_id != current_user["id"] and current_user["role"] != "admin":
        certificate_data.user_id = current_user["id"]

    # Criar o certificado
    certificate = await certificate_service.create_certificate(certificate_data)

    return certificate


@router.get("/{certificate_id}", response_model=CertificateDetail)
async def get_certificate(
    certificate_id: str = Path(..., description="ID do certificado"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna um certificado específico pelo ID.

    Requer autenticação. Apenas o próprio usuário pode acessar seus certificados.
    """
    certificate_service = CertificateService(db)

    # Buscar o certificado
    certificate = await certificate_service.get_certificate_detail(certificate_id)

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificado não encontrado"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if certificate.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a acessar este certificado"
        )

    return certificate


@router.get("/{certificate_id}/pdf", status_code=status.HTTP_200_OK)
async def get_certificate_pdf(
    certificate_id: str = Path(..., description="ID do certificado"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Gera e retorna o PDF do certificado.

    Requer autenticação. Apenas o próprio usuário pode acessar seus certificados.
    """
    certificate_service = CertificateService(db)

    # Buscar o certificado
    certificate = await certificate_service.get_certificate_detail(certificate_id)

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificado não encontrado"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if certificate.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a acessar este certificado"
        )

    # Gerar o PDF do certificado
    try:
        pdf_binary = await certificate_service.generate_certificate_pdf(certificate_id)

        # Incrementar o contador de downloads
        await certificate_service.increment_download_count(certificate_id)

        # Retornar o PDF como download
        return Response(
            content=pdf_binary,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="certificado-{certificate_id}.pdf"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar o PDF do certificado: {str(e)}"
        )


@router.get("/plan/{plan_id}", response_model=Optional[CertificateDetail])
async def get_certificate_by_plan(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna o certificado de conclusão relacionado a um plano específico.

    Útil para verificar se o usuário já tem certificado para um plano.
    Requer autenticação.
    """
    certificate_service = CertificateService(db)

    # Buscar certificado para este plano e usuário
    certificate = await certificate_service.get_certificate_by_plan_and_user(
        user_id=current_user["id"],
        plan_id=plan_id
    )

    return certificate  # Pode ser None se não existir certificado


@router.delete("/{certificate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certificate(
    certificate_id: str = Path(..., description="ID do certificado"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Exclui um certificado existente.

    Requer autenticação. Apenas o próprio usuário ou admin pode excluir certificados.
    """
    certificate_service = CertificateService(db)

    # Buscar o certificado existente
    existing_certificate = await certificate_service.get_certificate_by_id(certificate_id)

    if not existing_certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificado não encontrado"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if existing_certificate.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a excluir este certificado"
        )

    # Excluir o certificado
    await certificate_service.delete_certificate(certificate_id)

    return None
