from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "5766a3181d38"
down_revision: Union[str, Sequence[str], None] = "b4961534f8ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("referring_doctor_id", sa.Integer(), nullable=False),
        sa.Column("specialist_doctor_id", sa.Integer(), nullable=False),
        sa.Column("exam_type", sa.String(length=20), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["referring_doctor_id"], ["doctors.id"]),
        sa.ForeignKeyConstraint(["specialist_doctor_id"], ["doctors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "disease_episodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("doctor_id", sa.Integer(), nullable=True),
        sa.Column("diagnosis", sa.String(length=200), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["doctor_id"], ["doctors.id"]),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("disease_episodes")
    op.drop_table("appointments")
