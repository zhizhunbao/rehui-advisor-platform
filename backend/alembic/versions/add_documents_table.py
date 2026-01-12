"""Add documents table for Document Store pattern

Revision ID: add_documents_table_001
Revises: 
Create Date: 2026-01-12

This migration adds the documents table for flexible data storage.
All business data can be stored in this single table with JSONB.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


revision = "add_documents_table_001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create documents table
    op.create_table(
        "documents",
        sa.Column("id", UUID(as_uuid=False), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("data", JSONB, nullable=False, server_default="{}"),
        sa.Column("owner_id", UUID(as_uuid=False), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("tags", JSONB, nullable=True, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    
    # Basic indexes
    op.create_index("ix_documents_type", "documents", ["type"])
    op.create_index("ix_documents_status", "documents", ["status"])
    op.create_index("ix_documents_owner_id", "documents", ["owner_id"])
    op.create_index("ix_documents_created_at", "documents", ["created_at"])
    
    # Composite indexes for common queries
    op.create_index("ix_documents_type_status", "documents", ["type", "status"])
    op.create_index("ix_documents_type_owner", "documents", ["type", "owner_id"])
    
    # GIN indexes for JSONB fields
    op.execute("CREATE INDEX ix_documents_data_gin ON documents USING GIN(data)")
    op.execute("CREATE INDEX ix_documents_tags_gin ON documents USING GIN(tags)")
    
    # Grant permissions to Supabase roles
    op.execute("GRANT ALL ON documents TO service_role")
    op.execute("GRANT SELECT ON documents TO authenticated")
    op.execute("GRANT SELECT ON documents TO anon")


def downgrade() -> None:
    op.drop_index("ix_documents_tags_gin", table_name="documents")
    op.drop_index("ix_documents_data_gin", table_name="documents")
    op.drop_index("ix_documents_type_owner", table_name="documents")
    op.drop_index("ix_documents_type_status", table_name="documents")
    op.drop_index("ix_documents_created_at", table_name="documents")
    op.drop_index("ix_documents_owner_id", table_name="documents")
    op.drop_index("ix_documents_status", table_name="documents")
    op.drop_index("ix_documents_type", table_name="documents")
    op.drop_table("documents")
