import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

target = os.getenv("DB_TARGET", "local").lower()

url_local = os.getenv("DATABASE_URL_LOCAL")
url_supabase = os.getenv("DATABASE_URL_SUPABASE")

DATABASE_URL = url_supabase if target == "supabase" else url_local

if not DATABASE_URL:
    raise RuntimeError("Missing DATABASE_URL_LOCAL / DATABASE_URL_SUPABASE in .env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass
