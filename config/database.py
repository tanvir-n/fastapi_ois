from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'mysql+pymysql://root:12345678@localhost:3306/oxford_fastapi'

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)
