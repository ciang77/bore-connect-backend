from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import settings

machine_engine = create_engine(
    settings.machine_database_url,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)

MachineSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=machine_engine)

MachineBase = declarative_base()


def get_machine_db():
    db = MachineSessionLocal()
    try:
        yield db
    finally:
        db.close()
