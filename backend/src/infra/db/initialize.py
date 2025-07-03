from sqlalchemy.exc import OperationalError
from infra.db.database import Base, engine, SessionLocal
from infra.db.models import User
from utils.auth import AuthUtils
from core.settings import settings


def create_database():
    """Cria todas as tabelas do banco de dados."""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Banco de dados verificado/criado")
    except OperationalError as e:
        print(f"❌ Erro ao conectar/criar banco: {e}")


def create_admin_user():
    """Cria ou atualiza um usuário admin padrão."""
    db = SessionLocal()
    try:
        username = settings.INITIAL_USER_LOGIN_JWT
        email = settings.INITIAL_USER_EMAIL_JWT
        hashed_password = AuthUtils.get_password_hash(settings.INITIAL_USER_PASSWORD_JWT)

        # Busca por usuário existente com MESMO username ou MESMO email
        admin = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if admin:
            # Atualiza o usuário encontrado
            admin.username = username
            admin.email = email
            admin.hashed_password = hashed_password
            admin.is_active = True
            admin.user_type = "admin"
            db.commit()
            db.refresh(admin)
            print(f"🔄 Usuário admin atualizado: {admin.email}")
        else:
            # Cria novo usuário admin
            admin_user = User(
                username=username,
                email=email,
                hashed_password=hashed_password,
                is_active=True,
                user_type="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"✅ Usuário admin criado: {admin_user.email}")
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar/atualizar usuário admin: {e}")
    finally:
        db.close()



def initialize():
    """Executa os processos de inicialização: criar banco e admin."""
    create_database()
    create_admin_user()
