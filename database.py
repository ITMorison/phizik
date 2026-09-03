from contextlib import contextmanager
from pathlib import Path
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = f"sqlite:///{Path(__file__).with_name('ecopack.db')}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
_init_lock = Lock()


class Base(DeclarativeBase):
    pass


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    from models import Experiment, MassMeasurement, QualityCriteria, Sample, WeightSetting

    with _init_lock:
        try:
            Base.metadata.create_all(bind=engine, checkfirst=True)
        except OperationalError as error:
            # Two Render/Streamlit workers can race during first SQLite initialization.
            if "already exists" not in str(error).lower():
                raise


def get_session():
    return SessionLocal()
