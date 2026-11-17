import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from sqlalchemy.engine import URL

load_dotenv()
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")

DB_MSHOST=os.getenv("DB_MSHOST")
DB_MSPORT=os.getenv("DB_MSPORT")
DB_MSUSER=os.getenv("DB_MSUSER")
DB_MSPASSWORD=os.getenv("DB_MSPASSWORD")
DB_MSNAME=os.getenv("DB_MSNAME")

DATABASE_URL =URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

engine = create_engine(
    DATABASE_URL,pool_pre_ping=True,
    echo=True
)
DATABASE_URLMS=URL.create(
    drivername="mssql+pymssql",
    username=DB_MSUSER,
    password=DB_MSPASSWORD,
    host=DB_MSHOST,
    port=int(DB_MSPORT),
    database=DB_MSNAME
)

ms_engine=create_engine(
    DATABASE_URLMS,pool_pre_ping=True,echo=True
)

SessionLocal=sessionmaker(
    bind=engine,autoflush=False,autocommit=False
)

SessionMs=sessionmaker(
    bind=ms_engine,autoflush=False,autocommit=False

)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()