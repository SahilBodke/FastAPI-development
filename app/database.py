from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

 # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Connecting to database using postgres driver (Not required since we are now connecting using sqlalchemy)
# while True:
#     try:
#         connection = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'sahilPostgres', cursor_factory = RealDictCursor)

#         cursor = connection.cursor()   # Used to execute SQL statements
#         print("Successfully connected to database")
#         break

#     except Exception as error:
#         print("Failed to connect to database")
#         print("Error: ", error)
#         time.sleep(2)