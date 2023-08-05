"""Delete the file table.

Revision ID: 83ada95132bf
Revises: 459a0d7b8f09
Create Date: 2020-12-07 12:49:48.797794

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# pylint: skip-file

# revision identifiers, used by Alembic.
revision = "83ada95132bf"
down_revision = "459a0d7b8f09"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "pyfunceble_status",
        "file_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=True,
    )
    op.drop_constraint(
        "pyfunceble_status_ibfk_1", "pyfunceble_status", type_="foreignkey"
    )
    op.drop_index("path", table_name="pyfunceble_file")
    # op.drop_table('pyfunceble_file')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        "pyfunceble_status_ibfk_1",
        "pyfunceble_status",
        "pyfunceble_file",
        ["file_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.alter_column(
        "pyfunceble_status",
        "file_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False,
    )
    op.create_table(
        "pyfunceble_file",
        sa.Column(
            "id", mysql.INTEGER(display_width=11), autoincrement=True, nullable=False
        ),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("modified", mysql.DATETIME(), nullable=True),
        sa.Column("path", mysql.TEXT(collation="utf8mb4_unicode_ci"), nullable=False),
        sa.Column(
            "test_completed",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.CheckConstraint("`test_completed` in (0,1)", name="CONSTRAINT_1"),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("path", "pyfunceble_file", ["path"], unique=True)
    # ### end Alembic commands ###
