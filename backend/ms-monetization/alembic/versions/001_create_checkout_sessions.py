"""create checkout sessions table

Revision ID: 001
Revises: 
Create Date: 2024-03-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'checkout_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('session_id', sa.String(), nullable=False),
        sa.Column('payment_gateway', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('payment_id', sa.String(), nullable=True),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id')
    )
    op.create_index(op.f('ix_checkout_sessions_id'),
                    'checkout_sessions', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_checkout_sessions_id'),
                  table_name='checkout_sessions')
    op.drop_table('checkout_sessions')
