from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.settings import settings
from sqlalchemy.exc import OperationalError

Base = declarative_base()

# Construção condicional da URL do banco
if settings.DB_DRIVERNAME == "sqlite":
    DATABASE_URL = f"sqlite:///{settings.DB_DATABASENAME}"
    connect_args = {"check_same_thread": False}
else:
    DATABASE_URL = (
        f"{settings.DB_DRIVERNAME}://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASENAME}"
    )
    connect_args = {}

# Criação do engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Criação do session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função de dependência para uso com FastAPI ou manual
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
