"""Create shortened_url table

Revision ID: cb5180c3f02b
Revises: b7ab0e32d23d
Create Date: 2025-01-07 18:06:24.958046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel # Add SQLModel


# revision identifiers, used by Alembic.
revision: str = 'cb5180c3f02b'
down_revision: Union[str, None] = 'b7ab0e32d23d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shortened_url',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_short_code_custom', sa.Boolean(), nullable=True),
    sa.Column('short_code', sa.VARCHAR(length=20), nullable=False),
    sa.Column('original_url', sa.VARCHAR(length=2083), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shortened_url')
    # ### end Alembic commands ###
