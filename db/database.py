from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config
from db.models import Base

# Create SQLite engine with thread check disabled for Streamlit multithreading
engine = create_engine(
    f"sqlite:///{config.SQLITE_DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize SQLite database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
