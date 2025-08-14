
"""
Revision ID: 650459092949
Revises: 
Create Date: 2025-08-13
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '650459092949'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
	op.create_table(
		'items',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('nome', sa.String(length=100)),
		sa.Column('descricao', sa.String(length=255)),
	)

def downgrade():
	op.drop_table('items')

