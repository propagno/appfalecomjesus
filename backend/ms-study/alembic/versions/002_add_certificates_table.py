"""add certificates table and update study models

Revision ID: 002
Revises: 001
Create Date: 2024-03-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.exc import ProgrammingError

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def table_exists(table_name):
    """Verifica se a tabela já existe no banco de dados"""
    try:
        conn = op.get_bind()
        result = conn.execute(sa.text(
            f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}'"))
        return result.scalar() is not None
    except:
        return False


def upgrade() -> None:
    # Atualizar tabela study_plans - adicionando novos campos
    if table_exists('study_plans'):
        try:
            # Verificar se as colunas não existem antes de adicionar
            conn = op.get_bind()
            for column_name in ['category', 'difficulty', 'image_url']:
                has_column = conn.execute(sa.text(
                    f"SELECT 1 FROM information_schema.columns WHERE table_name = 'study_plans' AND column_name = '{column_name}'")).scalar() is not None
                if not has_column:
                    op.add_column('study_plans', sa.Column(
                        column_name, sa.String(), nullable=True))
        except Exception as e:
            print(f"Erro ao adicionar colunas em study_plans: {e}")
            # Continuar mesmo se houver erro

    # Criar tabela certificates, que é a única nova tabela
    if not table_exists('certificates'):
        try:
            op.create_table(
                'certificates',
                sa.Column('id', postgresql.UUID(as_uuid=True),
                          primary_key=True, default=uuid.uuid4),
                sa.Column('user_id', postgresql.UUID(
                    as_uuid=True), nullable=False),
                sa.Column('study_plan_id', postgresql.UUID(
                    as_uuid=True), nullable=False),
                sa.Column('certificate_code', sa.String(),
                          nullable=False, unique=True),
                sa.Column('completed_at', sa.DateTime(), nullable=False,
                          server_default=sa.text('NOW()')),
                sa.Column('download_count', sa.Integer(),
                          nullable=False, server_default='0'),
                sa.Column('created_at', sa.DateTime(), nullable=False,
                          server_default=sa.text('NOW()')),
                sa.Column('updated_at', sa.DateTime(), nullable=False,
                          server_default=sa.text('NOW()')),
                sa.ForeignKeyConstraint(
                    ['study_plan_id'], ['study_plans.id'], ondelete='CASCADE'),
                sa.PrimaryKeyConstraint('id'),
            )
            print("Tabela certificates criada com sucesso")
        except Exception as e:
            print(f"Erro ao criar tabela certificates: {e}")

    # Adicionar índices para melhorar performance (verificando existência antes)
    try:
        # Criar índices apenas em tabelas que existem e apenas se o índice não existir
        indices = [
            ('idx_certificates_user_id', 'certificates', 'user_id'),
            ('idx_certificates_code', 'certificates', 'certificate_code'),
            ('idx_study_plans_user_id', 'study_plans', 'user_id'),
            ('idx_study_sections_plan_id', 'study_sections', 'study_plan_id'),
            ('idx_study_content_section_id', 'study_content', 'section_id')
        ]

        conn = op.get_bind()
        for idx_name, table_name, column_name in indices:
            # Só tenta criar o índice se a tabela existir
            if table_exists(table_name):
                # Verificar se o índice já existe
                index_exists = conn.execute(sa.text(
                    f"SELECT 1 FROM pg_indexes WHERE indexname = '{idx_name}'")).scalar() is not None
                if not index_exists:
                    op.create_index(idx_name, table_name, [column_name])
                    print(f"Índice {idx_name} criado com sucesso")
    except Exception as e:
        print(f"Erro ao criar alguns índices: {e}")
        # Continuar mesmo se houver erro


def downgrade() -> None:
    # Remover tabelas na ordem inversa
    try:
        op.drop_table('certificates')
    except:
        pass

    # Remover índices (ignorando erros)
    try:
        op.drop_index('idx_certificates_user_id', table_name='certificates')
        op.drop_index('idx_certificates_code', table_name='certificates')
        op.drop_index('idx_study_content_section_id',
                      table_name='study_content')
        op.drop_index('idx_study_sections_plan_id',
                      table_name='study_sections')
        op.drop_index('idx_study_plans_user_id', table_name='study_plans')
    except:
        pass

    # Remover colunas adicionadas (ignorando erros)
    try:
        op.drop_column('study_plans', 'image_url')
        op.drop_column('study_plans', 'difficulty')
        op.drop_column('study_plans', 'category')
    except:
        pass
