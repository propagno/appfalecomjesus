import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse, RedirectResponse

from app.schemas.certificate import (
    Certificate,
    CertificateList,
    ShareCertificateRequest,
    ShareCertificateResponse
)
from app.services.certificate_service import CertificateService
from app.api.deps import get_certificate_service, get_current_user


router = APIRouter()


@router.get(
    "/",
    response_model=CertificateList,
    status_code=status.HTTP_200_OK,
    summary="Listar certificados do usuário"
)
async def list_certificates(
    skip: int = 0,
    limit: int = 20,
    current_user=Depends(get_current_user),
    certificate_service: CertificateService = Depends(get_certificate_service)
) -> Any:
    """
    Lista todos os certificados do usuário autenticado.
    """
    return await certificate_service.get_user_certificates(current_user.id, skip, limit)


@router.get(
    "/{certificate_id}",
    response_model=Certificate,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de um certificado"
)
async def get_certificate(
    certificate_id: uuid.UUID,
    current_user=Depends(get_current_user),
    certificate_service: CertificateService = Depends(get_certificate_service)
) -> Any:
    """
    Obtém os detalhes de um certificado específico.
    """
    certificate = await certificate_service.get_certificate_by_id(certificate_id)

    if not certificate or certificate.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificado não encontrado"
        )

    return certificate


@router.get(
    "/by-code/{certificate_code}",
    response_model=Certificate,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de um certificado pelo código"
)
async def get_certificate_by_code(
    certificate_code: str,
    certificate_service: CertificateService = Depends(get_certificate_service)
) -> Any:
    """
    Obtém os detalhes de um certificado pelo código.
    Não requer autenticação para permitir verificação pública.
    """
    certificate = await certificate_service.get_certificate_by_code(certificate_code)

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificado não encontrado"
        )

    return certificate


@router.post(
    "/generate-for-completed",
    response_model=List[Certificate],
    status_code=status.HTTP_201_CREATED,
    summary="Gerar certificados para planos concluídos"
)
async def generate_certificates_for_completed_plans(
    current_user=Depends(get_current_user),
    certificate_service: CertificateService = Depends(get_certificate_service)
) -> Any:
    """
    Verifica todos os planos concluídos e gera certificados para os que ainda não têm.
    """
    certificates = await certificate_service.check_and_generate_for_completed_plans(current_user.id)

    # Converter para lista de schemas
    cert_schemas = []
    for cert in certificates:
        cert_schema = Certificate.from_orm(cert)
        cert_schemas.append(cert_schema)

    return cert_schemas


@router.get(
    "/{certificate_id}/download",
    summary="Baixar o certificado em PDF"
)
async def download_certificate(
    certificate_id: uuid.UUID,
    current_user=Depends(get_current_user),
    certificate_service: CertificateService = Depends(get_certificate_service)
) -> Any:
    """
    Baixa o certificado em formato PDF.
    """
    certificate = await certificate_service.get_certificate_by_id(certificate_id)

    if not certificate or str(certificate.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificado não encontrado"
        )

    file_path, file_name = await certificate_service.download_certificate(certificate_id)

    if not file_path:
        # Se não tivermos um arquivo gerado, retornamos uma mensagem
        # Em uma implementação real, aqui você geraria o PDF sob demanda
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo do certificado não disponível. Por favor, tente novamente mais tarde."
        )

    # Se for uma URL externa, redirecionamos
    if file_path.startswith(('http://', 'https://')):
        return RedirectResponse(url=file_path)

    # Caso contrário, retornamos o arquivo
    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/pdf"
    )


@router.post(
    "/{certificate_id}/share",
    response_model=ShareCertificateResponse,
    status_code=status.HTTP_200_OK,
    summary="Compartilhar certificado"
)
async def share_certificate(
    certificate_id: uuid.UUID,
    request: ShareCertificateRequest,
    current_user=Depends(get_current_user),
    certificate_service: CertificateService = Depends(get_certificate_service)
) -> Any:
    """
    Compartilha o certificado em redes sociais.
    """
    certificate = await certificate_service.get_certificate_by_id(certificate_id)

    if not certificate or str(certificate.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificado não encontrado"
        )

    return await certificate_service.share_certificate(certificate_id, request)
