import logging
from logging.handlers import RotatingFileHandler
import os
from core.settings import settings

# Cria a pasta de logs se não existir
log_dir = os.path.abspath("/system_logs")
os.makedirs(log_dir, exist_ok=True)

# Caminho do arquivo de log
log_file = os.path.join(log_dir, f"{settings.CONTAINER_NAME}.log")

# Configura o handler de log com rotação (limite de 10 MB)
handler = RotatingFileHandler(
    log_file,
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=1,              # Mantém 12 arquivos de backup
    encoding="utf-8"
)

# Formato dos logs
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
handler.setFormatter(formatter)

# Logger global
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)  # Pode ser DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.addHandler(handler)
logger.propagate = False
