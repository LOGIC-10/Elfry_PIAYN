此目錄包含資料庫連線設定與schema定義

│  └─ db/
│     ├─ __init__.py
│     ├─ database.py             # SQLAlchemy資料庫連線與session管理
│     └─ schemas.py              # 如果需要SQLAlchemy的schema或Alembic遷移，可放這裡