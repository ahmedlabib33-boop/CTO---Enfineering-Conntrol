# Migrations

The local MVP uses SQLAlchemy metadata initialization for first-run simplicity.
Before production deployment, introduce Alembic migration scripts and disable metadata auto-creation in production.
