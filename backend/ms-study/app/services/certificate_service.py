import os
import uuid
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from io import BytesIO
from pathlib import Path

import httpx
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader
from weasyprint.text.fonts import FontConfiguration

from app.repositories.certificate_repository import CertificateRepository
from app.repositories.study_plan_repository import StudyPlanRepository
from app.repositories.user_study_progress_repository import UserStudyProgressRepository
from app.models.certificate import Certificate
from app.schemas.certificate import ShareCertificateRequest, ShareCertificateResponse, CertificateList, Certificate as CertificateSchema, CertificateCreate, CertificateDetail
from app.core.config import settings
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import desc, asc
from sqlalchemy.sql import func

# Configurar logger
logger = logging.getLogger(__name__)

# Importar WeasyPrint de forma segura
try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
    logging.info("WeasyPrint importado com sucesso. PDFs serão gerados.")
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logging.warning(
        "WeasyPrint não está disponível. Serão gerados apenas certificados em texto.")


class CertificateService:
    """
    Serviço para gerenciamento de certificados.
    """

    def __init__(
        self,
        certificate_repository: CertificateRepository,
        study_plan_repository: StudyPlanRepository,
        user_study_progress_repository: UserStudyProgressRepository,
        user_service: UserService,
        db: Session
    ):
        self.certificate_repository = certificate_repository
        self.study_plan_repository = study_plan_repository
        self.user_study_progress_repository = user_study_progress_repository
        self.user_service = user_service
        self.db = db

        # Configurar o ambiente Jinja2 para os templates de certificados
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.template_env = Environment(
            loader=FileSystemLoader(self.template_dir))

        # Criar diretório de armazenamento de certificados, se não existir
        os.makedirs(settings.CERTIFICATE_STORAGE_PATH, exist_ok=True)

    async def generate_certificate(self, user_id: uuid.UUID, study_plan_id: uuid.UUID) -> Optional[Certificate]:
        """
        Gera um certificado para um plano de estudo concluído.

        Args:
            user_id: ID do usuário
            study_plan_id: ID do plano de estudo

        Returns:
            Optional[Certificate]: O certificado gerado ou None se não for possível gerar
        """
        try:
            # Verificar se já existe um certificado para este plano
            existing_certificate = await self.certificate_repository.get_for_study_plan(user_id, study_plan_id)
            if existing_certificate:
                logger.info(
                    f"Certificado para plano {study_plan_id} do usuário {user_id} já existe")
                return existing_certificate

            # Verificar se o usuário concluiu o plano de estudo
            progress = await self.user_study_progress_repository.get_by_user_and_plan(
                user_id=user_id,
                study_plan_id=study_plan_id
            )

            if not progress or progress.completion_percentage < 100:
                logger.warning(
                    f"Tentativa de gerar certificado para plano não concluído: user_id={user_id}, study_plan_id={study_plan_id}")
                return None

            # Buscar informações do plano de estudo
            study_plan = await self.study_plan_repository.get_by_id(study_plan_id)
            if not study_plan:
                logger.error(
                    f"Plano de estudo não encontrado: study_plan_id={study_plan_id}")
                return None

            # Criar certificado
            certificate_data = {
                "user_id": user_id,
                "study_plan_id": study_plan_id,
                "completed_at": datetime.utcnow()
            }

            certificate = await self.certificate_repository.create(certificate_data)
            logger.info(
                f"Certificado gerado com sucesso: {certificate.id} para plano {study_plan_id} do usuário {user_id}")

            # Gerar o PDF do certificado (salvar no armazenamento)
            await self._generate_certificate_pdf(certificate.id)

            return certificate

        except Exception as e:
            logger.exception(
                f"Erro ao gerar certificado para plano {study_plan_id} do usuário {user_id}: {str(e)}")
            return None

    async def get_user_certificates(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> CertificateList:
        """
        Obtém todos os certificados de um usuário.

        Args:
            user_id: ID do usuário
            skip: Quantidade de itens para pular (paginação)
            limit: Quantidade máxima de itens a retornar

        Returns:
            CertificateList: Lista de certificados e total
        """
        certificates = await self.certificate_repository.get_by_user_id(user_id, skip, limit)
        total = await self.certificate_repository.count_by_user_id(user_id)

        # Converter para o schema e adicionar títulos dos planos de estudo
        certificate_schemas = []
        for cert in certificates:
            cert_schema = CertificateSchema.from_orm(cert)
            if hasattr(cert, 'study_plan') and cert.study_plan:
                cert_schema.study_plan_title = cert.study_plan.title
            certificate_schemas.append(cert_schema)

        return CertificateList(
            certificates=certificate_schemas,
            total=total
        )

    async def get_certificate_by_id(self, certificate_id: uuid.UUID) -> Optional[CertificateSchema]:
        """
        Obtém um certificado pelo ID.

        Args:
            certificate_id: ID do certificado

        Returns:
            Optional[CertificateSchema]: O certificado encontrado ou None
        """
        certificate = await self.certificate_repository.get_by_id(certificate_id)

        if not certificate:
            return None

        cert_schema = CertificateSchema.from_orm(certificate)
        if hasattr(certificate, 'study_plan') and certificate.study_plan:
            cert_schema.study_plan_title = certificate.study_plan.title

        return cert_schema

    async def get_certificate_by_code(self, certificate_code: str) -> Optional[CertificateSchema]:
        """
        Obtém um certificado pelo código.

        Args:
            certificate_code: Código do certificado

        Returns:
            Optional[CertificateSchema]: O certificado encontrado ou None
        """
        certificate = await self.certificate_repository.get_by_code(certificate_code)

        if not certificate:
            return None

        cert_schema = CertificateSchema.from_orm(certificate)
        if hasattr(certificate, 'study_plan') and certificate.study_plan:
            cert_schema.study_plan_title = certificate.study_plan.title

        return cert_schema

    async def download_certificate(self, certificate_id: uuid.UUID) -> Tuple[Optional[str], Optional[str]]:
        """
        Prepara o certificado para download e incrementa o contador.

        Args:
            certificate_id: ID do certificado

        Returns:
            Tuple[Optional[str], Optional[str]]: Tupla com o caminho do arquivo e o nome do arquivo, ou None, None
        """
        certificate = await self.certificate_repository.get_by_id(certificate_id)

        if not certificate:
            return None, None

        # Incrementar contador de downloads
        await self.certificate_repository.increment_download_count(certificate_id)

        # Por enquanto, se já tiver uma URL de imagem, a usamos
        if certificate.image_url:
            return certificate.image_url, f"certificado_{certificate.certificate_code}.pdf"

        # Caso contrário, precisamos gerar o PDF do certificado (em implementação futura)
        # Em uma implementação real, aqui você chamaria um serviço para gerar o PDF
        # Por enquanto, vamos retornar None
        return None, None

    async def share_certificate(self, certificate_id: uuid.UUID, request: ShareCertificateRequest) -> ShareCertificateResponse:
        """
        Compartilha um certificado em redes sociais.

        Args:
            certificate_id: ID do certificado
            request: Dados do compartilhamento

        Returns:
            ShareCertificateResponse: Resposta do compartilhamento
        """
        certificate = await self.certificate_repository.get_by_id(certificate_id)

        if not certificate:
            return ShareCertificateResponse(
                success=False,
                message="Certificado não encontrado"
            )

        # Incrementar contador de compartilhamentos
        await self.certificate_repository.increment_shared_count(certificate_id)

        # Gerar URL para compartilhamento
        base_url = settings.FRONTEND_URL
        share_url = f"{base_url}/certificates/view/{certificate.certificate_code}"

        # Mensagem padrão se não for fornecida
        message = request.message or f"Concluí o curso '{certificate.title}' na plataforma FaleComJesus!"

        # Gerar URLs específicas para cada rede social
        if request.social_network == "whatsapp":
            share_url = f"https://wa.me/?text={message}%20{share_url}"
        elif request.social_network == "facebook":
            share_url = f"https://www.facebook.com/sharer/sharer.php?u={share_url}&quote={message}"
        elif request.social_network == "twitter":
            share_url = f"https://twitter.com/intent/tweet?text={message}&url={share_url}"
        elif request.social_network == "email":
            share_url = f"mailto:?subject=Meu certificado FaleComJesus&body={message}%20{share_url}"

        return ShareCertificateResponse(
            success=True,
            share_url=share_url,
            message=f"Compartilhamento preparado para {request.social_network}"
        )

    async def check_and_generate_for_completed_plans(self, user_id: uuid.UUID) -> List[Certificate]:
        """
        Verifica todos os planos concluídos e gera certificados para os que ainda não têm.

        Args:
            user_id: ID do usuário

        Returns:
            List[Certificate]: Lista de certificados gerados
        """
        # Buscar todos os progressos com 100% de conclusão
        progress_list = await self.user_study_progress_repository.get_completed_by_user(user_id)

        generated_certificates = []
        for progress in progress_list:
            # Verificar se já existe certificado para este plano
            exists = await self.certificate_repository.check_if_exists(user_id, progress.study_plan_id)

            if not exists:
                certificate = await self.generate_certificate(user_id, progress.study_plan_id)
                if certificate:
                    generated_certificates.append(certificate)

        return generated_certificates

    async def _generate_certificate_pdf(self, certificate_id: uuid.UUID) -> bool:
        """
        Gera o PDF de um certificado e o salva no armazenamento.

        Args:
            certificate_id: ID do certificado.

        Returns:
            True se o PDF foi gerado com sucesso, False caso contrário.
        """
        try:
            # Buscar dados do certificado
            result = await self.certificate_repository.get_by_id(certificate_id)
            if not result:
                logger.error(
                    f"Certificado {certificate_id} não encontrado para geração de PDF")
                return False

            cert, plan = result

            # Obter o nome do usuário
            user_name = await self.user_service.get_user_name(cert.user_id)

            # Dados para o template
            template_data = {
                "certificate_code": cert.certificate_code,
                "user_name": user_name,
                "plan_title": plan.title,
                "completion_date": cert.completed_at.strftime("%d/%m/%Y"),
                "certificate_id": str(cert.id)
            }

            # Renderizar o HTML do certificado
            template = self.template_env.get_template("certificate.html")
            html_content = template.render(**template_data)

            # Converter HTML para PDF com WeasyPrint
            html = HTML(string=html_content)
            css = CSS(string="""
                @page {
                    size: A4 landscape;
                    margin: 0;
                }
                body {
                    margin: 0;
                    padding: 0;
                }
            """)

            pdf_output = html.write_pdf(stylesheets=[css])

            # Salvar o PDF no armazenamento
            pdf_path = os.path.join(
                settings.CERTIFICATE_STORAGE_PATH, f"{certificate_id}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_output)

            logger.info(
                f"PDF do certificado {certificate_id} gerado com sucesso em {pdf_path}")
            return True

        except Exception as e:
            logger.exception(
                f"Erro ao gerar PDF do certificado {certificate_id}: {str(e)}")
            return False

    async def get_user_certificates(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "completion_date",
        sort_desc: bool = True
    ) -> Tuple[List[CertificateSchema], int]:
        """
        Retorna os certificados do usuário com paginação.

        Args:
            user_id: ID do usuário
            skip: Itens para pular (paginação)
            limit: Máximo de itens para retornar
            sort_by: Campo para ordenação
            sort_desc: Se True, ordenação decrescente; se False, crescente

        Returns:
            Tupla com a lista de certificados e o total de certificados
        """
        # Construir query base
        query = select(Certificate).where(Certificate.user_id == user_id)

        # Contar total para paginação
        count_query = select(Certificate).where(Certificate.user_id == user_id)
        result = await self.db.execute(count_query)
        total = len(result.scalars().all())

        # Ordenar resultados
        if hasattr(Certificate, sort_by):
            order_column = getattr(Certificate, sort_by)
            if sort_desc:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))
        else:
            # Ordenação padrão se o campo não existir
            query = query.order_by(desc(Certificate.completion_date))

        # Aplicar paginação
        query = query.offset(skip).limit(limit)

        # Executar a consulta
        result = await self.db.execute(query)
        certificates = result.scalars().all()

        # Converter para o schema
        certificate_details = [CertificateSchema.from_orm(
            cert) for cert in certificates]

        return certificate_details, total

    async def create_certificate(self, data: CertificateCreate) -> CertificateDetail:
        """
        Cria um novo certificado de conclusão.

        Args:
            data: Dados do certificado a ser criado

        Returns:
            Certificado criado
        """
        # Verificar se já existe um certificado para este plano e usuário
        existing_query = select(Certificate).where(
            (Certificate.user_id == data.user_id) &
            (Certificate.plan_id == data.plan_id)
        )
        result = await self.db.execute(existing_query)
        existing = result.scalars().first()

        if existing:
            # Atualizar o existente com novos dados
            existing.completion_date = data.completion_date or datetime.utcnow()
            existing.verse = data.verse
            existing.verse_reference = data.verse_reference
            existing.plan_title = data.plan_title
            existing.user_name = data.user_name
            await self.db.commit()
            await self.db.refresh(existing)

            return CertificateDetail.model_validate(existing)

        # Gerar código único para o certificado
        certificate_code = f"FCJ-{str(uuid.uuid4())[:8].upper()}"

        # Criar novo certificado
        new_certificate = Certificate(
            id=str(uuid.uuid4()),
            user_id=data.user_id,
            plan_id=data.plan_id,
            completion_date=data.completion_date or datetime.utcnow(),
            certificate_code=certificate_code,
            download_count=0,
            verse=data.verse,
            verse_reference=data.verse_reference,
            plan_title=data.plan_title,
            user_name=data.user_name,
            created_at=datetime.utcnow()
        )

        self.db.add(new_certificate)
        await self.db.commit()
        await self.db.refresh(new_certificate)

        return CertificateDetail.model_validate(new_certificate)

    async def get_certificate_by_id(self, certificate_id: str) -> Optional[Certificate]:
        """
        Retorna um certificado pelo ID.

        Args:
            certificate_id: ID do certificado

        Returns:
            Certificado encontrado ou None
        """
        query = select(Certificate).where(Certificate.id == certificate_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_certificate_detail(self, certificate_id: str) -> Optional[CertificateDetail]:
        """
        Retorna os detalhes de um certificado pelo ID.

        Args:
            certificate_id: ID do certificado

        Returns:
            Detalhes do certificado ou None
        """
        certificate = await self.get_certificate_by_id(certificate_id)
        if not certificate:
            return None

        return CertificateDetail.model_validate(certificate)

    async def delete_certificate(self, certificate_id: str) -> bool:
        """
        Exclui um certificado pelo ID.

        Args:
            certificate_id: ID do certificado

        Returns:
            True se excluído com sucesso, False caso contrário
        """
        certificate = await self.get_certificate_by_id(certificate_id)

        if not certificate:
            return False

        await self.db.delete(certificate)
        await self.db.commit()

        return True

    async def get_certificate_by_plan_and_user(
        self,
        user_id: str,
        plan_id: str
    ) -> Optional[CertificateSchema]:
        """
        Retorna o certificado de um usuário para um plano específico.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano

        Returns:
            Detalhes do certificado ou None
        """
        query = select(Certificate).where(
            (Certificate.user_id == user_id) &
            (Certificate.plan_id == plan_id)
        )

        result = await self.db.execute(query)
        certificate = result.scalars().first()

        if not certificate:
            return None

        return CertificateSchema.from_orm(certificate)

    async def increment_download_count(self, certificate_id: str) -> bool:
        """
        Incrementa o contador de downloads do certificado.

        Args:
            certificate_id: ID do certificado

        Returns:
            True se atualizado com sucesso, False caso contrário
        """
        certificate = await self.get_certificate_by_id(certificate_id)

        if not certificate:
            return False

        certificate.download_count += 1
        await self.db.commit()

        return True

    async def generate_certificate_pdf(self, certificate_id: str) -> bytes:
        """
        Gera o PDF do certificado.

        Em uma implementação real, isso usaria uma biblioteca como ReportLab ou WeasyPrint
        para gerar um PDF bonito, ou chamaria um serviço externo como Microservice.

        Args:
            certificate_id: ID do certificado

        Returns:
            PDF do certificado em binário
        """
        certificate = await self.get_certificate_detail(certificate_id)

        if not certificate:
            raise ValueError("Certificado não encontrado")

        try:
            # Exemplo: chamada para um microservice de geração de PDF (mock)
            # Na implementação real, isso seria integrado com um serviço de geração de PDF

            # Opção 1: Gerar o PDF localmente com uma biblioteca
            pdf_data = self._generate_pdf_locally(certificate)
            return pdf_data

            # Opção 2: Chamar um microservice dedicado (exemplo)
            # return await self._call_pdf_service(certificate)

        except Exception as e:
            logger.error(f"Erro ao gerar PDF do certificado: {str(e)}")
            raise

    def _generate_pdf_locally(self, certificate: CertificateDetail) -> bytes:
        """
        Gera um PDF simples localmente usando uma biblioteca como ReportLab.

        Esta é uma implementação de exemplo/mock. Em uma aplicação real,
        você precisaria instalar e usar uma biblioteca como ReportLab ou WeasyPrint.

        Args:
            certificate: Detalhes do certificado

        Returns:
            PDF do certificado em binário
        """
        # Simulação: em uma implementação real, este código geraria um PDF real
        # Usando uma biblioteca como ReportLab:
        #
        # from reportlab.pdfgen import canvas
        # from reportlab.lib.pagesizes import A4
        # from reportlab.lib.units import cm
        #
        # buffer = BytesIO()
        # c = canvas.Canvas(buffer, pagesize=A4)
        #
        # # Adicionar conteúdo ao PDF
        # c.setFont("Helvetica", 24)
        # c.drawCentredString(A4[0]/2, A4[1]-5*cm, "CERTIFICADO DE CONCLUSÃO")
        #
        # c.setFont("Helvetica", 16)
        # c.drawCentredString(A4[0]/2, A4[1]-8*cm, f"Certifica-se que {certificate.user_name}")
        # c.drawCentredString(A4[0]/2, A4[1]-10*cm, f"concluiu com sucesso o plano de estudos:")
        # c.drawCentredString(A4[0]/2, A4[1]-12*cm, f"{certificate.plan_title}")
        #
        # c.setFont("Helvetica", 12)
        # c.drawCentredString(A4[0]/2, A4[1]-16*cm, f"Data de conclusão: {certificate.completion_date.strftime('%d/%m/%Y')}")
        # c.drawCentredString(A4[0]/2, A4[1]-17*cm, f"Código de validação: {certificate.certificate_code}")
        #
        # c.setFont("Helvetica-Italic", 14)
        # c.drawCentredString(A4[0]/2, A4[1]-20*cm, f'"{certificate.verse}"')
        # c.drawCentredString(A4[0]/2, A4[1]-21*cm, f"{certificate.verse_reference}")
        #
        # c.save()
        # pdf_data = buffer.getvalue()
        # buffer.close()
        # return pdf_data

        # Simulação para desenvolvimento (retorna um PDF simples)
        pdf_content = f"""
        CERTIFICADO DE CONCLUSÃO
        
        Certifica-se que {certificate.user_name}
        concluiu com sucesso o plano de estudos:
        
        {certificate.plan_title}
        
        Data de conclusão: {certificate.completion_date.strftime('%d/%m/%Y')}
        Código de validação: {certificate.certificate_code}
        
        "{certificate.verse}"
        {certificate.verse_reference}
        """.encode('utf-8')

        return pdf_content

    async def _call_pdf_service(self, certificate: CertificateDetail) -> bytes:
        """
        Chama um microsserviço dedicado para geração de PDF.

        Esta é uma implementação de exemplo. Em uma aplicação real, você precisaria
        configurar um serviço dedicado para geração de PDF.

        Args:
            certificate: Detalhes do certificado

        Returns:
            PDF do certificado em binário
        """
        # URL do microservice responsável pela geração de PDFs
        pdf_service_url = settings.PDF_SERVICE_URL

        # Preparar dados para enviar ao serviço
        payload = {
            "certificate_id": certificate.id,
            "user_name": certificate.user_name,
            "plan_title": certificate.plan_title,
            "completion_date": certificate.completion_date.isoformat(),
            "certificate_code": certificate.certificate_code,
            "verse": certificate.verse,
            "verse_reference": certificate.verse_reference,
            "template": "certificate"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{pdf_service_url}/generate",
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.content

        except httpx.RequestError as e:
            logger.error(f"Erro na comunicação com o serviço de PDF: {str(e)}")
            raise Exception(f"Falha ao conectar ao serviço de PDF: {str(e)}")

        except httpx.HTTPStatusError as e:
            logger.error(f"Erro na resposta do serviço de PDF: {str(e)}")
            raise Exception(f"O serviço de PDF retornou erro: {str(e)}")

        except Exception as e:
            logger.error(f"Erro desconhecido ao gerar PDF: {str(e)}")
            raise Exception(f"Falha ao gerar PDF: {str(e)}")

    def list_certificates(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "completion_date",
        sort_desc: bool = True
    ) -> Tuple[List[CertificateDetail], int]:
        """
        Retorna os certificados do usuário com paginação.
        """
        query = select(Certificate).where(Certificate.user_id == user_id)

        # Ordenação
        if sort_by == "completion_date":
            query = query.order_by(desc(Certificate.completion_date) if sort_desc else asc(
                Certificate.completion_date))

        # Paginação
        result = db.execute(query.offset(skip).limit(limit))
        certificates = result.scalars().all()

        # Contagem total
        total_query = select(func.count()).select_from(
            Certificate).where(Certificate.user_id == user_id)
        total = db.execute(total_query).scalar_one()

        # Converter para o schema
        certificate_details = [CertificateDetail.model_validate(
            cert) for cert in certificates]

        return certificate_details, total

    async def get_user_certificate_for_plan(
        self,
        user_id: str,
        plan_id: str
    ) -> Optional[CertificateDetail]:
        """
        Retorna o certificado de um usuário para um plano específico.
        """
        query = select(Certificate).where(
            (Certificate.user_id == user_id) &
            (Certificate.plan_id == plan_id)
        )

        result = await self.db.execute(query)
        certificate = result.scalars().first()

        if not certificate:
            return None

        return CertificateDetail.model_validate(certificate)

    def _generate_certificate_file(self, certificate_id: int, user_name: str,
                                   plan_title: str, completion_date: datetime,
                                   certificate_code: str) -> str:
        """
        Gera o arquivo de certificado (PDF ou TXT).

        Args:
            certificate_id: ID do certificado
            user_name: Nome do usuário
            plan_title: Título do plano
            completion_date: Data de conclusão
            certificate_code: Código do certificado

        Returns:
            str: Caminho para o arquivo gerado
        """
        if WEASYPRINT_AVAILABLE:
            return self._generate_pdf_certificate(
                certificate_id, user_name, plan_title,
                completion_date, certificate_code
            )
        else:
            return self._generate_text_certificate(
                certificate_id, user_name, plan_title,
                completion_date, certificate_code
            )

    def _generate_pdf_certificate(self, certificate_id: int, user_name: str,
                                  plan_title: str, completion_date: datetime,
                                  certificate_code: str) -> str:
        """
        Gera um certificado em PDF usando WeasyPrint.
        """
        try:
            # Caminho para salvar o PDF
            pdf_path = f"{settings.CERTIFICATE_STORAGE_PATH}/certificate_{certificate_id}.pdf"

            # Ler o template HTML e substituir as variáveis
            with open(self.template_dir / "certificate.html", 'r') as f:
                html_template = f.read()

            # Substituir variáveis no template
            html_content = html_template.replace('{{user_name}}', user_name)
            html_content = html_content.replace('{{plan_title}}', plan_title)
            html_content = html_content.replace(
                '{{completion_date}}', completion_date.strftime("%d/%m/%Y"))
            html_content = html_content.replace(
                '{{certificate_code}}', certificate_code)

            # Configurar fontes e CSS
            font_config = FontConfiguration()

            # Gerar PDF
            HTML(string=html_content).write_pdf(
                pdf_path,
                font_config=font_config
            )

            logger.info(f"Certificado PDF gerado com sucesso: {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.error(f"Erro ao gerar PDF do certificado: {str(e)}")
            # Fallback para certificado em texto em caso de erro
            return self._generate_text_certificate(
                certificate_id, user_name, plan_title,
                completion_date, certificate_code
            )

    def _generate_text_certificate(self, certificate_id: int, user_name: str,
                                   plan_title: str, completion_date: datetime,
                                   certificate_code: str) -> str:
        """
        Gera um certificado em texto simples como fallback.
        """
        try:
            # Caminho para salvar o arquivo de texto
            text_path = f"{settings.CERTIFICATE_STORAGE_PATH}/certificate_{certificate_id}.txt"

            # Criar conteúdo do certificado em texto
            certificate_text = f"""
            =======================================
                      CERTIFICADO
            =======================================
            
            Certificamos que
            
            {user_name}
            
            concluiu com sucesso o plano de estudos
            
            "{plan_title}"
            
            em {completion_date.strftime("%d/%m/%Y")}
            
            Código de verificação: {certificate_code}
            =======================================
            """

            # Salvar arquivo
            with open(text_path, 'w') as f:
                f.write(certificate_text)

            logger.info(
                f"Certificado em texto gerado com sucesso: {text_path}")
            return text_path
        except Exception as e:
            logger.error(f"Erro ao gerar certificado em texto: {str(e)}")
            return ""
