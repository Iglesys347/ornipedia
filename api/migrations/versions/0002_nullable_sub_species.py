"""make translations.sub_species nullable

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-13

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002"
down_revision: Union[str, Sequence[str], None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("translations") as batch_op:
        batch_op.alter_column("sub_species", existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    op.execute("UPDATE translations SET sub_species = '' WHERE sub_species IS NULL")
    with op.batch_alter_table("translations") as batch_op:
        batch_op.alter_column("sub_species", existing_type=sa.String(), nullable=False)
