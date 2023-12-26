"""adicionando relacionamento entre repertorio e colecao

Revision ID: ed1b17322ed3
Revises: a0f683873d88
Create Date: 2023-12-26 11:09:05.244030

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ed1b17322ed3'
down_revision = 'a0f683873d88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Tema_repertorio',
    sa.Column('tema_id', sa.Integer(), nullable=True),
    sa.Column('repertorio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['repertorio_id'], ['repertorio.id'], ),
    sa.ForeignKeyConstraint(['tema_id'], ['tema.id'], )
    )
    op.drop_table('colecao_repertorio')
    with op.batch_alter_table('colecao', schema=None) as batch_op:
        batch_op.drop_constraint('colecao_ibfk_2', type_='foreignkey')
        batch_op.drop_column('repertorio_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('colecao', schema=None) as batch_op:
        batch_op.add_column(sa.Column('repertorio_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('colecao_ibfk_2', 'repertorio', ['repertorio_id'], ['id'])

    op.create_table('colecao_repertorio',
    sa.Column('my_row_id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('colecao_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('repertorio_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['colecao_id'], ['colecao.id'], name='colecao_repertorio_ibfk_1'),
    sa.ForeignKeyConstraint(['repertorio_id'], ['repertorio.id'], name='colecao_repertorio_ibfk_2'),
    sa.PrimaryKeyConstraint('my_row_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('Tema_repertorio')
    op.drop_table('Colecao_repertorio')
    # ### end Alembic commands ###