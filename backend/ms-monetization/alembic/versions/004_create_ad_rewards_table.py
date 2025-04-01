"""create ad rewards table

Revision ID: 004
Revises: 003
Create Date: 2024-03-23 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar enum AdType
    op.execute("CREATE TYPE adtype AS ENUM ('video', 'banner')")

    # Criar enum RewardType
    op.execute("CREATE TYPE rewardtype AS ENUM ('chat_messages', 'study_days')")

    # Criar tabela ad_rewards
    op.create_table(
        'ad_rewards',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ad_type', postgresql.ENUM('video', 'banner',
                  name='adtype'), nullable=False),
        sa.Column('reward_type', postgresql.ENUM('chat_messages', 'study_days',
                  name='rewardtype'), nullable=False),
        sa.Column('reward_value', sa.Integer(), nullable=False),
        sa.Column('watched_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('ad_rewards')
    op.execute('DROP TYPE rewardtype')
    op.execute('DROP TYPE adtype')
