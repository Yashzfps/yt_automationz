from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.entities import VideoAsset


def test_video_fingerprint_unique_constraint() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(
            VideoAsset(
                source_path="/tmp/a.mp4",
                fingerprint="dup",
                file_name="a.mp4",
                extension=".mp4",
                size_bytes=1,
                valid=True,
            )
        )
        session.commit()

        session.add(
            VideoAsset(
                source_path="/tmp/b.mp4",
                fingerprint="dup",
                file_name="b.mp4",
                extension=".mp4",
                size_bytes=1,
                valid=True,
            )
        )
        try:
            session.commit()
            raise AssertionError("expected unique constraint failure")
        except IntegrityError:
            session.rollback()
