import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Cargamos las variables secretas del archivo .env
load_dotenv()

# 2. Leemos la URL de Supabase
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Creamos el motor. 
# IMPORTANTE: Como ya no es SQLite, sacamos el 'connect_args' que teníamos antes.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()