"""initial

Revision ID: 001
Revises: 
Create Date: 2024-02-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chat_history',
        sa.Column('id', UUID(as_uuid=True),
                  primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('response', sa.Text(), nullable=False),
        sa.Column('model_used', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()')),
        sa.Column('tokens_used', sa.Integer(), nullable=False, default=0),
        sa.Column('context_length', sa.Integer(), nullable=False, default=0)
    )

    op.create_index('idx_chat_history_user_id', 'chat_history', ['user_id'])
    op.create_index('idx_chat_history_created_at',
                    'chat_history', ['created_at'])


def downgrade():
    op.drop_index('idx_chat_history_created_at')
    op.drop_index('idx_chat_history_user_id')
    op.drop_table('chat_history')
