"""generate certificates for completed plans

Revision ID: 003
Revises: 002
Create Date: 2024-03-25 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column, select, func, text
import uuid
import random
import string
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

# Definição de tabelas para consulta SQL
study_plans = table(
    'study_plans',
    column('id', postgresql.UUID),
    column('title', sa.String)
)

user_study_progress = table(
    'user_study_progress',
    column('id', postgresql.UUID),
    column('user_id', postgresql.UUID),
    column('study_plan_id', postgresql.UUID),
    column('completion_percentage', sa.Float)
)

certificates = table(
    'certificates',
    column('id', postgresql.UUID),
    column('user_id', postgresql.UUID),
    column('study_plan_id', postgresql.UUID),
    column('certificate_code', sa.String),
    column('completed_at', sa.DateTime),
    column('download_count', sa.Integer),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime)
)


def generate_certificate_code(length=12):
    """Gera um código único para o certificado."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def upgrade() -> None:
    # Conectar ao banco de dados
    connection = op.get_bind()

    # Encontrar planos de estudo concluídos (completion_percentage = 100)
    completed_plans_query = sa.select([
        user_study_progress.c.user_id,
        user_study_progress.c.study_plan_id,
        study_plans.c.title
    ]).select_from(
        user_study_progress.join(
            study_plans,
            user_study_progress.c.study_plan_id == study_plans.c.id
        )
    ).where(
        user_study_progress.c.completion_percentage >= 100.0
    )

    completed_plans = connection.execute(completed_plans_query).fetchall()

    # Gerar certificados para planos concluídos
    for user_id, study_plan_id, plan_title in completed_plans:
        # Verificar se já existe um certificado para este plano/usuário
        existing_cert_query = sa.select([certificates.c.id]).where(
            sa.and_(
                certificates.c.user_id == user_id,
                certificates.c.study_plan_id == study_plan_id
            )
        )

        existing_cert = connection.execute(existing_cert_query).first()

        # Se não existir certificado, criar um novo
        if not existing_cert:
            cert_id = uuid.uuid4()
            cert_code = generate_certificate_code()
            now = datetime.utcnow()

            # Inserir novo certificado
            connection.execute(
                certificates.insert().values(
                    id=cert_id,
                    user_id=user_id,
                    study_plan_id=study_plan_id,
                    certificate_code=cert_code,
                    completed_at=now,
                    download_count=0,
                    created_at=now,
                    updated_at=now
                )
            )

            print(
                f"Certificado gerado para plano '{plan_title}' do usuário {user_id}")


def downgrade() -> None:
    # Remover certificados gerados por esta migração
    # Observação: não é possível saber exatamente quais foram gerados pela migração,
    # então não implementamos o downgrade para evitar perda de dados
    pass
