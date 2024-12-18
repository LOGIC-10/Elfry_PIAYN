from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, JSON, Boolean, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    conversations = relationship("Conversation", back_populates="user")

class Tool(Base):
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    return_char_limit = Column(Integer, default=6000)
    description = Column(Text, nullable=False)
    tags = Column(JSON, default=lambda: ["base"])
    source_type = Column(String(50))
    json_schema = Column(JSON, nullable=False)
    source_code = Column(Text)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    request_data = Column(JSON)
    response_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="conversations")

class ModelsAPI(Base):
    __tablename__ = "models_api"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    provider = Column(String, index=True)
    api_key = Column(String)
    base_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expire_time = Column(DateTime)
    is_active = Column(Boolean, default=True)
    config = Column(JSON, nullable=True)  # For additional configuration

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)
