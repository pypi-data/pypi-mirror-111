"""Add inactive table.

Revision ID: 3d6f4a33cdb2
Revises: 7bcf7fa64ba1
Create Date: 2020-12-13 19:45:41.893657

"""
import sqlalchemy as sa
from alembic import op

# pylint: skip-file


# revision identifiers, used by Alembic.
revision = "3d6f4a33cdb2"
down_revision = "7bcf7fa64ba1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pyfunceble_inactive",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("modified_at", sa.DateTime(), nullable=True),
        sa.Column("idna_subject", sa.Text(), nullable=False),
        sa.Column("checker_type", sa.String(length=50), nullable=False),
        sa.Column("destination", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("tested_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("pyfunceble_inactive")
    # ### end Alembic commands ###
