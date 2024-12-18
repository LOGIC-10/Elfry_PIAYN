此目錄為整個專案的根目錄，包含主要程式碼與需求檔案
├─ app/
│  ├─ main.py                    # 整個API的入口
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ tools.py                # Tools主要API入口
│  │  ├─ chat.py                 # Chat主要API入口
│  │  ├─ embedding.py            # Embedding主要API入口
│  │  └─ database.py             # Database相關API入口
│  │
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ tools_service.py        # Tools邏輯實現，包括Search、WebScraper、Calculate函數
│  │  ├─ chat_service.py         # Chat邏輯實現，呼叫OpenAI API
│  │  ├─ embedding_service.py    # Embedding邏輯實現，呼叫OpenAI Embedding API
│  │  └─ database_service.py     # Database邏輯實現，操作Conversations、Tools、Users資料表
│  │
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ database_models.py      # SQLAlchemy的ORM Model: Conversations、Tools、Users等表
│  │  ├─ request_response.py     # Pydantic的Request/Response模型
│  │  └─ openai_models.py        # 對OpenAI API的request/response結構定義(如需要)
│  │
│  └─ db/
│     ├─ __init__.py
│     ├─ database.py             # SQLAlchemy資料庫連線與session管理
│     └─ schemas.py              # 如果需要SQLAlchemy的schema或Alembic遷移，可放這裡
│
└─ requirements.txt