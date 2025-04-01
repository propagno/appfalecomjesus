"""create plans table

Revision ID: 002
Revises: 001
Create Date: 2024-03-23 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar tabela plans
    op.create_table(
        'plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price_monthly', sa.Integer(),
                  nullable=False),  # em centavos
        sa.Column('price_yearly', sa.Integer(), nullable=False),  # em centavos
        sa.Column('features', postgresql.JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Inserir planos padrão
    op.execute("""
        INSERT INTO plans (id, name, description, price_monthly, price_yearly, features)
        VALUES 
        (
            '11111111-1111-1111-1111-111111111111',
            'Free',
            'Acesso básico ao sistema',
            0,
            0,
            '{"chat_messages_per_day": 5, "study_days_per_month": 10, "has_ads": true}'
        ),
        (
            '22222222-2222-2222-2222-222222222222',
            'Premium',
            'Acesso ilimitado a todos os recursos',
            2990,
            29900,
            '{"chat_messages_per_day": -1, "study_days_per_month": -1, "has_ads": false}'
        )
    """)


def downgrade() -> None:
    op.drop_table('plans')
