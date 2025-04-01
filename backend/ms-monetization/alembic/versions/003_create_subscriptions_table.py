"""create subscriptions table

Revision ID: 003
Revises: 002
Create Date: 2024-03-23 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar enum SubscriptionStatus
    op.execute(
        "CREATE TYPE subscriptionstatus AS ENUM ('active', 'canceled', 'expired')")

    # Criar tabela subscriptions
    op.create_table(
        'subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', postgresql.ENUM('active', 'canceled', 'expired',
                  name='subscriptionstatus'), nullable=False),
        sa.Column('payment_gateway', postgresql.ENUM(
            'Stripe', 'Hotmart', name='paymentgateway'), nullable=True),
        sa.Column('payment_id', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('subscriptions')
    op.execute('DROP TYPE subscriptionstatus')
