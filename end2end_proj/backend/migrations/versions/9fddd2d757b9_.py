"""empty message

Revision ID: 9fddd2d757b9
Revises: 9df48b28986a
Create Date: 2024-04-23 23:59:03.328707

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9fddd2d757b9"
down_revision: Union[str, None] = "9df48b28986a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("disabled", sa.Boolean(), nullable=True))
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=True)
    )
    op.drop_column("users", "disabled")
    # ### end Alembic commands ###
