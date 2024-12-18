
from sqlalchemy.orm import Session
from ..db.database import Tool
from .tools_service import search, webscraper, calculate

class ToolManager:
    _instance = None
    _tools = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def initialize_tools(cls, db: Session):
        """Load tools from database and map to actual functions"""
        default_tools = {
            "search": search,
            "webscraper": webscraper,
            "calculate": calculate
        }
        
        # Load tools from database
        db_tools = db.query(Tool).all()
        
        # If no tools in database, initialize with defaults
        if not db_tools:
            for name, func in default_tools.items():
                tool = Tool(
                    name=name,
                    description=func.__doc__ or "",
                    parameters={}  # You might want to add parameter schemas here
                )
                db.add(tool)
            db.commit()
            db_tools = db.query(Tool).all()

        # Map database tools to actual functions
        cls._tools = {
            tool.name: default_tools.get(tool.name)
            for tool in db_tools
            if tool.name in default_tools
        }

    @classmethod
    def get_tool(cls, name: str):
        return cls._tools.get(name)

    @classmethod
    def get_available_tools(cls):
        return list(cls._tools.keys())