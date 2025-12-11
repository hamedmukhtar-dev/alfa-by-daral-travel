alfa-by-daral-travel/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── wallet.py
│   │   │   └── service_request.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── auth.py
│   │   │   └── service_request.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── wallet.py
│   │   │   └── services.py
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── openai_client.py
│   │   │   └── intent_router.py
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── security.py
│   │       ├── hashing.py
│   │       └── logging_config.py
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend-web/   # سكِلتون واجهة ويب (تضيفه لاحقاً)
│   └── README.md
│
├── mobile/         # سكِلتون Flutter (تضيفه لاحقاً)
│   └── README.md
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── API_OVERVIEW.md
│
├── .env.example
├── .gitignore
└── README.md
