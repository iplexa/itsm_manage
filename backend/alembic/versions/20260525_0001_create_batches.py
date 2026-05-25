"""create batches and batch tasks

Revision ID: 20260525_0001
Revises:
Create Date: 2026-05-25 00:00:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260525_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


batch_status = postgresql.ENUM(
    "draft",
    "running",
    "done",
    "failed",
    name="batch_status",
    create_type=False,
)
batch_task_status = postgresql.ENUM(
    "draft",
    "pending",
    "running",
    "done",
    "failed",
    "skipped",
    name="batch_task_status",
    create_type=False,
)


def upgrade() -> None:
    postgresql.ENUM("draft", "running", "done", "failed", name="batch_status").create(
        op.get_bind(),
        checkfirst=True,
    )
    postgresql.ENUM(
        "draft",
        "pending",
        "running",
        "done",
        "failed",
        "skipped",
        name="batch_task_status",
    ).create(op.get_bind(), checkfirst=True)

    op.create_table(
        "batches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", batch_status, server_default="draft", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_batches_id"), "batches", ["id"], unique=False)

    op.create_table(
        "batch_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("desc", sa.Text(), nullable=False),
        sa.Column("service", sa.String(length=100), nullable=False),
        sa.Column("time_minutes", sa.Integer(), nullable=False),
        sa.Column("closure_text", sa.Text(), nullable=False),
        sa.Column("closure_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", batch_task_status, server_default="draft", nullable=False),
        sa.Column("itsm_request_id", sa.String(length=100), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_batch_tasks_batch_id"), "batch_tasks", ["batch_id"], unique=False)
    op.create_index(op.f("ix_batch_tasks_id"), "batch_tasks", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_batch_tasks_id"), table_name="batch_tasks")
    op.drop_index(op.f("ix_batch_tasks_batch_id"), table_name="batch_tasks")
    op.drop_table("batch_tasks")
    op.drop_index(op.f("ix_batches_id"), table_name="batches")
    op.drop_table("batches")
    batch_task_status.drop(op.get_bind(), checkfirst=True)
    batch_status.drop(op.get_bind(), checkfirst=True)
