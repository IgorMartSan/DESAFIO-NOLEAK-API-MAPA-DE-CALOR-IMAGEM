

Estrutura geral do projeto:

src/
├── api/
│   └── v1/endpoints/user.py             ✅ rotas
├── domain/
│   └── user/
│       ├── entities.py                  ✅ Enum e tipos
│       └── interfaces.py                ✅ Interface do repositório
├── infrastructure/
│   └── persistence/
│       ├── database.py                  ✅ engine, session
│       ├── models/user_model.py         ✅ SQLAlchemy User
│       └── repositories/user_repo.py    ✅ SQLUserRepository
├── services/
│   └── user_service.py                  ✅ lógica de aplicação
└── core/
    └── config/settings.py               ✅ DB config