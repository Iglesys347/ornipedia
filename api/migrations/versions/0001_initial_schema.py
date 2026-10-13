"""initial schema

Schema of the database as it was before Alembic was introduced. On an existing
database, mark it as applied with `alembic stamp 0001` before upgrading.

Revision ID: 0001
Revises:
Create Date: 2026-10-13

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "birds",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("latin_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_birds_id"), "birds", ["id"], unique=False)
    op.create_table(
        "image_authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("link", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "link", name="img_author_uc"),
    )
    op.create_index(op.f("ix_image_authors_id"), "image_authors", ["id"], unique=False)
    op.create_table(
        "image_licenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("link", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("short_name", "link", name="img_license_uc"),
    )
    op.create_index(op.f("ix_image_licenses_id"), "image_licenses", ["id"], unique=False)
    op.create_table(
        "translations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bird_id", sa.Integer(), nullable=False),
        sa.Column("language_code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("species", sa.String(), nullable=False),
        sa.Column("sub_species", sa.String(), nullable=False),
        sa.Column("details", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["bird_id"], ["birds.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_translations_id"), "translations", ["id"], unique=False)
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bird_id", sa.Integer(), nullable=False),
        sa.Column("license_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("image_path", sa.String(), nullable=False),
        sa.Column("original_url", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["image_authors.id"]),
        sa.ForeignKeyConstraint(["bird_id"], ["birds.id"]),
        sa.ForeignKeyConstraint(["license_id"], ["image_licenses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_images_id"), "images", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_images_id"), table_name="images")
    op.drop_table("images")
    op.drop_index(op.f("ix_translations_id"), table_name="translations")
    op.drop_table("translations")
    op.drop_index(op.f("ix_image_licenses_id"), table_name="image_licenses")
    op.drop_table("image_licenses")
    op.drop_index(op.f("ix_image_authors_id"), table_name="image_authors")
    op.drop_table("image_authors")
    op.drop_index(op.f("ix_birds_id"), table_name="birds")
    op.drop_table("birds")
