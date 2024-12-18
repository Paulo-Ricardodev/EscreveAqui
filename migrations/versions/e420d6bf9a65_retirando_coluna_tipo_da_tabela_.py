"""retirando coluna tipo da tabela repertório

Revision ID: e420d6bf9a65
Revises: 2ef520ae4604
Create Date: 2024-11-29 14:26:23.722468

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e420d6bf9a65'
down_revision = '2ef520ae4604'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Colecao_repertorio',
    sa.Column('colecao_id', sa.Integer(), nullable=True),
    sa.Column('repertorio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['colecao_id'], ['colecao.id'], ),
    sa.ForeignKeyConstraint(['repertorio_id'], ['repertorio.id'], )
    )
    op.create_table('Tema_repertorio',
    sa.Column('tema_id', sa.Integer(), nullable=True),
    sa.Column('repertorio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['repertorio_id'], ['repertorio.id'], ),
    sa.ForeignKeyConstraint(['tema_id'], ['tema.id'], )
    )
    op.create_table('tipo_repertorio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('repertorio_id', sa.Integer(), nullable=True),
    sa.Column('pontuacao', sa.Integer(), nullable=True),
    sa.Column('descricao', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['repertorio_id'], ['repertorio.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('colecao_repertorio')
    with op.batch_alter_table('repertorio', schema=None) as batch_op:
        batch_op.drop_column('tipo')

    with op.batch_alter_table('tema_repertorio', schema=None) as batch_op:
        batch_op.alter_column('tema_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('repertorio_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.drop_column('my_row_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tema_repertorio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('my_row_id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False))
        batch_op.alter_column('repertorio_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('tema_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('repertorio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo', mysql.VARCHAR(length=80), nullable=True))

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
    op.drop_table('tipo_repertorio')
    op.drop_table('Tema_repertorio')
    op.drop_table('Colecao_repertorio')
    # ### end Alembic commands ###
