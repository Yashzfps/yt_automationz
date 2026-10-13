from datetime import UTC, datetime

from sqlalchemy import text

from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import entities  # noqa: F401


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS schema_bootstrap (
                    id INTEGER PRIMARY KEY,
                    version TEXT NOT NULL,
                    applied_at TEXT NOT NULL
                )
                """
            )
        )
        exists = db.execute(text("SELECT COUNT(*) FROM schema_bootstrap")).scalar_one()
        if exists == 0:
            db.execute(
                text("INSERT INTO schema_bootstrap (version, applied_at) VALUES (:v, :a)"),
                {"v": "1", "a": datetime.now(UTC).isoformat()},
            )
        db.commit()


def recover_jobs_on_startup() -> None:
    with SessionLocal() as db:
        db.execute(
            text(
                """
                UPDATE workflow_jobs
                SET status='pending', stage='recovered', error_message='Recovered after service restart'
                WHERE status='running'
                """
            )
        )
        db.commit()
