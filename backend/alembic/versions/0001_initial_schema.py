"""Initial schema — all core tables (organizations, roles, permissions,
users, smes, assessments, predictions, reports, report_versions,
report_templates, audit_logs, notifications, assessment_history)

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-07-18

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("tenant_code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("industry", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_organizations_id", "organizations", ["id"])

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_roles_id", "roles", ["id"])

    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_permissions_id", "permissions", ["id"])

    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), primary_key=True),
        sa.Column("permission_id", sa.Integer(), sa.ForeignKey("permissions.id"), primary_key=True),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "smes",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("industry", sa.String(length=100), nullable=True),
        sa.Column("business_age_months", sa.Integer(), nullable=True),
        sa.Column("ownership_type", sa.String(length=100), nullable=True),
        sa.Column("registration_date", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_smes_id", "smes", ["id"])
    op.create_index("ix_smes_legal_name", "smes", ["legal_name"])
    op.create_index("ix_smes_industry", "smes", ["industry"])

    op.create_table(
        "assessments",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("sme_id", sa.Integer(), sa.ForeignKey("smes.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=True),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("risk_category", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="completed"),
        sa.Column("features_json", sa.JSON(), nullable=False),
        sa.Column("shap_values_json", sa.JSON(), nullable=False),
        sa.Column("recommendations_json", sa.JSON(), nullable=True),
        sa.Column("ai_insights", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_assessments_id", "assessments", ["id"])

    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("assessment_id", sa.Integer(), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("input_payload", sa.JSON(), nullable=False),
        sa.Column("output_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_predictions_id", "predictions", ["id"])

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("assessment_id", sa.Integer(), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("report_type", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="generated"),
        sa.Column("file_url", sa.String(length=500), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_reports_id", "reports", ["id"])

    op.create_table(
        "report_versions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("report_id", sa.Integer(), sa.ForeignKey("reports.id"), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("file_url", sa.String(length=500), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_report_versions_id", "report_versions", ["id"])

    op.create_table(
        "report_templates",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("template_type", sa.String(length=100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_report_templates_id", "report_templates", ["id"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("changes", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_audit_logs_id", "audit_logs", ["id"])

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.String(length=1000), nullable=True),
        sa.Column("notification_type", sa.String(length=100), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_notifications_id", "notifications", ["id"])

    op.create_table(
        "assessment_history",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("assessment_id", sa.Integer(), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("change_type", sa.String(length=100), nullable=False),
        sa.Column("changed_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("changes", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_assessment_history_id", "assessment_history", ["id"])


def downgrade() -> None:
    op.drop_table("assessment_history")
    op.drop_table("notifications")
    op.drop_table("audit_logs")
    op.drop_table("report_templates")
    op.drop_table("report_versions")
    op.drop_table("reports")
    op.drop_table("predictions")
    op.drop_table("assessments")
    op.drop_table("smes")
    op.drop_table("users")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
    op.drop_table("organizations")