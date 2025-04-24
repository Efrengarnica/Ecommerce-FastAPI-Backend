"""Agregando roles a mi modelo User

Revision ID: 4f03f81ff92d
Revises: 622873d7da5b
Create Date: 2025-04-22 22:37:50.042866

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql
from models.user import Role


# revision identifiers, used by Alembic.
revision = '4f03f81ff92d'
down_revision = '622873d7da5b'
branch_labels = None
depends_on = None


def upgrade():
    # Crear el tipo ENUM
    role_enum = postgresql.ENUM('client', 'admin', 'root', name='role')
    role_enum.create(op.get_bind())  # Aquí es donde se crea el tipo en la base de datos

    # Agregar la columna con ese tipo
    op.add_column('user', sa.Column('role', role_enum, nullable=False))


def downgrade():
    op.drop_column('user', 'role')

    # Borrar el tipo ENUM
    role_enum = postgresql.ENUM('client', 'admin', 'root', name='role')
    role_enum.drop(op.get_bind())   