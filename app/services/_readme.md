此目錄包含對應API邏輯的實作，包括與OpenAI交互及工具函數邏輯

│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ tools_service.py        # Tools邏輯實現，包括Search、WebScraper、Calculate函數
│  │  ├─ chat_service.py         # Chat邏輯實現，呼叫OpenAI API
│  │  ├─ embedding_service.py    # Embedding邏輯實現，呼叫OpenAI Embedding API
│  │  └─ database_service.py     # Database邏輯實現，操作Conversations、Tools、Users資料表
