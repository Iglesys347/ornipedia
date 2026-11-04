"""rename translations.species / sub_species to group_name / subgroup_name

"Rapaces" or "passereaux" are groups of birds, not species (each bird is a species).
("group" alone is a reserved SQL word, hence the "_name" suffix.)

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-04

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003"
down_revision: Union[str, Sequence[str], None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("translations") as batch_op:
        batch_op.alter_column(
            "species", new_column_name="group_name", existing_type=sa.String(), existing_nullable=False
        )
        batch_op.alter_column(
            "sub_species", new_column_name="subgroup_name", existing_type=sa.String(), existing_nullable=True
        )


def downgrade() -> None:
    with op.batch_alter_table("translations") as batch_op:
        batch_op.alter_column(
            "group_name", new_column_name="species", existing_type=sa.String(), existing_nullable=False
        )
        batch_op.alter_column(
            "subgroup_name", new_column_name="sub_species", existing_type=sa.String(), existing_nullable=True
        )
