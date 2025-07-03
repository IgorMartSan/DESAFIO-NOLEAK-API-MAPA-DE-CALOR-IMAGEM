from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from infra.db.initialize import create_database, create_admin_user
from contextlib import asynccontextmanager
from domain.user.routes import router as user_router
from domain.auth.routes import router as auth_router
from domain.external_api.routes import router as external_api_router 
from colorama import Fore, Style
from core.logger_config import logger
import uvicorn
import os
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Inicializando recursos...")
    # 👉 Executa na startup (antes da API começar a aceitar requisições)
    create_database()
    create_admin_user()
    # Aqui você poderia também abrir conexões com Redis, Mongo, Kafka, etc.
    yield
    # 👆 O yield separa o que é startup (acima) do que é shutdown (abaixo)
    print("🧹 Fechando recursos...")
    # 👉 Executa na shutdown (quando a API está desligando)
    # Fechar conexões com banco, Redis, encerrar consumidores, etc.

# Instancia FastAPI
app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="API para criação, atualização e exclusão de usuários.",
    lifespan=lifespan
)

# 🌍 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou defina como settings.ALLOWED_ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 Rotas
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(external_api_router)

# 🧾 Middleware de log
@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    print(
        f"{Fore.BLUE}INFO: {request.method} {request.url.path} -> "
        f"{end_time - start_time:.4f}s{Style.RESET_ALL}"
    )
    print(f"{Fore.YELLOW}RAIZ DO PROJETO: {os.getcwd()}{Style.RESET_ALL}")
    return response

# 🔥 Execução local
if __name__ == "__main__":
    try:
        #logger.info("🟢 Servidor iniciando...")
        uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True, workers=6)
    except Exception as e:
        #logger.critical(f"🔥 Server crashed with error: {str(e)}", exc_info=True)
        pass
    

