"""add_domain_categories_table

Revision ID: add_domain_categories_001
Revises: d29879f29da6
Create Date: 2025-12-31

Create domain_categories table and add category_id to domains table.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_domain_categories_001"
down_revision: Union[str, None] = "d29879f29da6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create domain_categories table
    op.create_table(
        "domain_categories",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("name_en", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("description_en", sa.Text(), nullable=True),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("color", sa.String(50), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_domain_categories_code"),
    )
    op.create_index("ix_domain_categories_is_active", "domain_categories", ["is_active"], unique=False)
    op.create_index("ix_domain_categories_sort_order", "domain_categories", ["sort_order"], unique=False)

    # Add category_id to domains table
    op.add_column("domains", sa.Column("category_id", sa.UUID(as_uuid=False), nullable=True))
    op.create_index("ix_domains_category_id", "domains", ["category_id"], unique=False)
    op.create_foreign_key(
        "fk_domains_category_id",
        "domains",
        "domain_categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Add code column to domains if not exists
    op.add_column("domains", sa.Column("code", sa.String(50), nullable=True))
    op.create_index("ix_domains_code", "domains", ["code"], unique=True)

    # Add prompt columns to domains if not exists
    op.add_column("domains", sa.Column("prompt", sa.Text(), nullable=True))
    op.add_column("domains", sa.Column("prompt_en", sa.Text(), nullable=True))

    # Grant permissions
    op.execute("GRANT ALL ON domain_categories TO service_role")
    op.execute("GRANT SELECT ON domain_categories TO authenticated")
    op.execute("GRANT SELECT ON domain_categories TO anon")

    # Insert initial category data
    op.execute("""
        INSERT INTO domain_categories (code, name, name_en, icon, color, sort_order) VALUES
        ('travel', '出行旅游', 'Travel', 'Plane', 'bg-blue-500', 1),
        ('living', '生活服务', 'Living', 'Home', 'bg-green-500', 2),
        ('career', '职业发展', 'Career', 'Briefcase', 'bg-purple-500', 3),
        ('finance', '金融理财', 'Finance', 'DollarSign', 'bg-amber-500', 4),
        ('education', '教育学习', 'Education', 'GraduationCap', 'bg-indigo-500', 5)
    """)


def downgrade() -> None:
    op.drop_constraint("fk_domains_category_id", "domains", type_="foreignkey")
    op.drop_index("ix_domains_category_id", table_name="domains")
    op.drop_column("domains", "category_id")
    op.drop_index("ix_domains_code", table_name="domains")
    op.drop_column("domains", "code")
    op.drop_column("domains", "prompt")
    op.drop_column("domains", "prompt_en")
    op.drop_index("ix_domain_categories_sort_order", table_name="domain_categories")
    op.drop_index("ix_domain_categories_is_active", table_name="domain_categories")
    op.drop_table("domain_categories")
