from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_IRL = "postgresql://<username>:<password>@<ipaddress>/hostname/<database_name>"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://" + settings.database_username + ":" + settings.database_password + "@" + settings.database_hostname + "/" + settings.database_name
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# Raw SQL(NO longer needded since we use sql alchemy)
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password123',
#         cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connected Successfully")
#         break
#     except Exception as e:
#         print("Database Connection Failed")
#         print("Error: ", e)
#         time.sleep(2)