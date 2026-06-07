from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import settings

engine = create_engine(
    settings.database_url,
    pool_size=settings.DB_POOL_SIZE,      # 20
    max_overflow=20,                       # 新增：峰值额外 20 个连接
    pool_recycle=3600,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
