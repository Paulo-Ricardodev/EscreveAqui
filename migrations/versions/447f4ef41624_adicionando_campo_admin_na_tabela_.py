"""Adicionando campo admin na tabela Usuario

Revision ID: 447f4ef41624
Revises: a2df9ab205d9
Create Date: 2023-12-04 20:11:35.552093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '447f4ef41624'
down_revision = 'a2df9ab205d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admins', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('admins')

    # ### end Alembic commands ###
