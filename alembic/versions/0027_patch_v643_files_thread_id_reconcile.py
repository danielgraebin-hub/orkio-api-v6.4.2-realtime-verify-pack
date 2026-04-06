"""PATCH v6.4.3 — files.thread_id reconcile

Revision ID: 0027_patch_v643_files_thread_id_reconcile
Revises: 0026_patch_v64_realtime_schema_reconcile
Create Date: 2026-04-06
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text as sa_text


revision = "0027_patch_v643_files_thread_id_reconcile"
down_revision = "0026_patch_v64_realtime_schema_reconcile"
branch_labels = None
depends_on = None


def _table_exists(conn, table_name: str) -> bool:
    row = conn.execute(
        sa_text(
            """
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = current_schema()
              AND table_name = :table_name
            LIMIT 1
            """
        ),
        {"table_name": table_name},
    ).fetchone()
    return row is not None


def _column_exists(conn, table_name: str, column_name: str) -> bool:
    row = conn.execute(
        sa_text(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = :table_name
              AND column_name = :column_name
            LIMIT 1
            """
        ),
        {"table_name": table_name, "column_name": column_name},
    ).fetchone()
    return row is not None


def _index_exists(conn, index_name: str) -> bool:
    row = conn.execute(
        sa_text(
            """
            SELECT 1
            FROM pg_indexes
            WHERE schemaname = current_schema()
              AND indexname = :index_name
            LIMIT 1
            """
        ),
        {"index_name": index_name},
    ).fetchone()
    return row is not None


def upgrade() -> None:
    conn = op.get_bind()

    if not _table_exists(conn, "files"):
        return

    if not _column_exists(conn, "files", "thread_id"):
        op.add_column("files", sa.Column("thread_id", sa.String(), nullable=True))

    if not _index_exists(conn, "ix_files_thread_id"):
        op.create_index("ix_files_thread_id", "files", ["thread_id"], unique=False)


def downgrade() -> None:
    conn = op.get_bind()

    if _table_exists(conn, "files") and _index_exists(conn, "ix_files_thread_id"):
        op.drop_index("ix_files_thread_id", table_name="files")

    if _table_exists(conn, "files") and _column_exists(conn, "files", "thread_id"):
        op.drop_column("files", "thread_id")
