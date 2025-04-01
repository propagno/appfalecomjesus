"""initial

Revision ID: 001
Revises: 
Create Date: 2025-03-24 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar enum PlanType
    op.execute("CREATE TYPE plantype AS ENUM ('free', 'mensal', 'anual')")

    # Criar enum PaymentGateway
    op.execute("CREATE TYPE paymentgateway AS ENUM ('Stripe', 'Hotmart')")

    # Criar tabela subscriptions
    op.create_table(
        'subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_type', postgresql.ENUM('free', 'mensal',
                  'anual', name='plantype'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('payment_gateway', postgresql.ENUM(
            'Stripe', 'Hotmart', name='paymentgateway'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela ad_rewards
    op.create_table(
        'ad_rewards',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('message_bonus', sa.Integer(), nullable=False),
        sa.Column('ad_provider', sa.String(), nullable=False),
        sa.Column('watched_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Remover tabelas
    op.drop_table('ad_rewards')
    op.drop_table('subscriptions')

    # Remover enums
    op.execute('DROP TYPE paymentgateway')
    op.execute('DROP TYPE plantype')
