import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega o .env e expande variáveis como ${VAR}
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=True)

class Settings:
    # Infra geral
    CONTAINER_NAME  = os.getenv("CONTAINER_NAME")
    IP = os.getenv("IP")
    #PREFIX_PORT = int(os.getenv("PREFIX_PORT"))
    GLOBAL_PATH = os.getenv("GLOBAL_PATH")
    PATH_LOGS = os.getenv("PATH_LOGS")
    PATH_VOL_POSTGRES = os.getenv("PATH_VOL_POSTGRES")

    # Postgres
    DB_DRIVERNAME = os.getenv("DB_DRIVERNAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_DATABASENAME = os.getenv("DB_DATABASENAME")
    DB_PORT = int(os.getenv("DB_PORT"))

    INITIAL_USER_LOGIN_JWT=os.getenv("INITIAL_USER_LOGIN_JWT")
    INITIAL_USER_PASSWORD_JWT=os.getenv("INITIAL_USER_PASSWORD_JWT")
    INITIAL_USER_EMAIL_JWT=os.getenv("INITIAL_USER_EMAIL_JWT")

    #PGADMIN_PORT = int(os.getenv("PGADMIN_PORT"))

    # Redis
    # REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    # REDIS_PORT = int(os.getenv("REDIS_PORT"))
    # REDIS_INSIGHT_PORT = int(os.getenv("REDIS_INSIGHT_PORT"))

    # JWT
    SECRET_KEY = "mysecretkey"
    ALGORITHM = "HS256"
    JWT_EXP_MINUTES = 30

# Instância global
settings = Settings()


