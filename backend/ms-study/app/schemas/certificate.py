from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, UUID4, Field, field_validator
from enum import Enum


class SocialNetwork(str, Enum):
    """Redes sociais suportadas para compartilhamento."""
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    EMAIL = "email"


class CertificateBase(BaseModel):
    """Modelo base para certificados."""
    user_id: str
    study_plan_id: str
    completion_date: datetime = None
    certificate_code: str = None
    verse_reference: Optional[str] = Field(
        None, description="Referência bíblica de inspiração")
    verse_text: Optional[str] = Field(
        None, description="Texto do versículo de inspiração")


class CertificateCreate(CertificateBase):
    """Modelo para criação de certificados."""
    pass


class CertificateInDB(CertificateBase):
    """Schema para certificado no banco de dados."""
    id: UUID4
    user_id: UUID4
    study_plan_id: UUID4
    completion_date: datetime
    image_url: Optional[str] = None
    download_count: int = 0
    shared_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Certificate(CertificateInDB):
    """Modelo simplificado de certificado."""
    id: int
    study_plan_title: Optional[str] = Field(
        None, description="Título do plano de estudo concluído")

    class Config:
        from_attributes = True


class CertificateRead(CertificateBase):
    """Schema para leitura de certificados."""
    id: str
    study_plan_title: str
    certificate_code: str
    completed_at: datetime
    download_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class CertificatePublicRead(BaseModel):
    """Schema para leitura pública de certificados (via código)."""
    user_name: str
    study_plan_title: str
    certificate_code: str
    completed_at: datetime

    class Config:
        from_attributes = True


class CertificateList(BaseModel):
    """Lista de certificados."""
    certificates: List[Certificate]
    count: int


class CertificateShare(BaseModel):
    """Schema para compartilhamento de certificados."""
    platform: str = Field(..., description="Plataforma para compartilhamento: 'whatsapp', 'facebook', 'twitter', 'instagram', 'linkedin'")
    message: Optional[str] = Field(
        None, description="Mensagem opcional para compartilhamento")


class CertificateShareResponse(BaseModel):
    """Schema de resposta para compartilhamento de certificados."""
    share_url: str
    platform: str


class CertificateUpdate(BaseModel):
    """Schema para atualização de certificados."""
    title: Optional[str] = Field(None, description="Título do certificado")
    description: Optional[str] = Field(
        None, description="Descrição detalhada do certificado")
    image_url: Optional[str] = Field(
        None, description="URL da imagem do certificado")
    download_count: Optional[int] = None
    verse_reference: Optional[str] = None
    verse_text: Optional[str] = None


class ShareCertificateRequest(BaseModel):
    """Schema para requisição de compartilhamento de certificado."""
    social_network: SocialNetwork = Field(...,
                                          description="Rede social para compartilhamento")
    message: Optional[str] = Field(
        None, description="Mensagem personalizada para compartilhamento")


class ShareCertificateResponse(BaseModel):
    """Schema para resposta de compartilhamento de certificado."""
    success: bool = Field(...,
                          description="Indicador de sucesso do compartilhamento")
    share_url: Optional[str] = Field(
        None, description="URL para compartilhamento direto")
    message: str = Field(...,
                         description="Mensagem sobre o resultado do compartilhamento")


class CertificateDetail(CertificateInDB):
    """Detalhe de certificado."""
    id: int
    user_id: str
    study_plan_id: str
    completion_date: datetime
    certificate_code: str
    created_at: datetime
    plan_title: str
    plan_description: Optional[str] = None
    plan_category: Optional[str] = None
    plan_difficulty: Optional[str] = None
    plan_duration_days: int
    user_name: Optional[str] = None  # Obtido do MS-Auth se disponível

    class Config:
        from_attributes = True


class CertificateListResponse(BaseModel):
    """Schema para resposta de listagem de certificados."""
    items: List[CertificateDetail]
    total: int
    page: int
    page_size: int


class CertificateValidationResponse(BaseModel):
    """Schema para validação de certificado."""
    is_valid: bool
    certificate: Optional[CertificateDetail] = None
    message: Optional[str] = None
