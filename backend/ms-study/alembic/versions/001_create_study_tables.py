"""create study tables

Revision ID: 001
Revises: 
Create Date: 2024-03-23 14:00:00.000000

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
    # Criar tabela study_plans sem dependência
    op.create_table(
        'study_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('duration_days', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela study_sections
    op.create_table(
        'study_sections',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('study_plan_id', postgresql.UUID(
            as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['study_plan_id'], ['study_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela study_content
    op.create_table(
        'study_content',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('section_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('content_type', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['section_id'], ['study_sections.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela user_study_progress sem dependência externa
    op.create_table(
        'user_study_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('study_plan_id', postgresql.UUID(
            as_uuid=True), nullable=False),
        sa.Column('current_section_id', postgresql.UUID(
            as_uuid=True), nullable=True),
        sa.Column('completion_percentage', sa.Float(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['study_plan_id'], ['study_plans.id'], ),
        sa.ForeignKeyConstraint(['current_section_id'], [
                                'study_sections.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('user_study_progress')
    op.drop_table('study_content')
    op.drop_table('study_sections')
    op.drop_table('study_plans')
