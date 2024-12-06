from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '5ecde3cc9b2d'
down_revision = 'ffb081129dc5'
branch_labels = None
depends_on = None

def column_exists(table_name, column_name, connection):
    inspector = Inspector.from_engine(connection)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns

def upgrade():
    connection = op.get_bind()
    if not column_exists('tema_repertorio', 'new_primary_key', connection):
        with op.batch_alter_table('tema_repertorio') as batch_op:
            batch_op.add_column(sa.Column('new_primary_key', sa.Integer))


