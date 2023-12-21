"""Migrando para a Azure

Revision ID: a2df9ab205d9
Revises: 
Create Date: 2023-12-04 19:52:26.575932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2df9ab205d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.create_table('tema_repertorio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tema_id', sa.Integer(), nullable=True),
    sa.Column('repertorio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['repertorio_id'], ['repertorio.id'], ),
    sa.ForeignKeyConstraint(['tema_id'], ['tema.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tipo_repertorio')
    op.drop_table('tema_repertorio')
    op.drop_table('comentario')
    op.drop_table('colecao')
    op.drop_table('tema')
    op.drop_table('repertorio')
    op.drop_table('usuario')
    # ### end Alembic commands ###
