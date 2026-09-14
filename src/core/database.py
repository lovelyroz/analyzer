from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

# مسیر فایل پایگاه داده SQLite
DATABASE_URL = "sqlite:///./tehran_stock.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# فعال‌سازی کلیدهای خارجی در SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()