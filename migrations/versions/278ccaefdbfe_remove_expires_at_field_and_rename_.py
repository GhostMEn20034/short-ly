"""Remove expires_at field and rename original_url field

Revision ID: 278ccaefdbfe
Revises: 4e07675244ae
Create Date: 2025-01-09 21:01:48.539614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel # Add SQLModel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '278ccaefdbfe'
down_revision: Union[str, None] = '4e07675244ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shortened_url', sa.Column('long_url', sa.VARCHAR(length=2083), nullable=False))
    op.drop_column('shortened_url', 'original_url')
    op.drop_column('shortened_url', 'expires_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shortened_url', sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.add_column('shortened_url', sa.Column('original_url', sa.VARCHAR(length=2083), autoincrement=False, nullable=False))
    op.drop_column('shortened_url', 'long_url')
    # ### end Alembic commands ###