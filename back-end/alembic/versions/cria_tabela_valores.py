"""
Migration para criar a tabela 'valores'.
"""
from alembic import op
import sqlalchemy as sa

revision = 'cria_tabela_valores'
down_revision = '650459092949'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'valores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('item_id', sa.Integer, sa.ForeignKey('items.id')),
        sa.Column('data_cadastro', sa.DateTime),
        sa.Column('valor', sa.Float),
    )

def downgrade():
    op.drop_table('valores')
