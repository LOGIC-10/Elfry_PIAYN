import inspect
import logging
from typing import Callable, List, Dict
from sqlalchemy.orm import Session
from .tool_schema import Tool
from .tools_service import search, webscraper, calculate

logger = logging.getLogger(__name__)

class ToolManager:
    _instance = None
    _tools = {}
    _schemas = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_or_create_tool_schema(cls, *target_functions: Callable) -> List[Dict]:
        schemas = []
        for target_function in target_functions:
            func_name = target_function.__name__
            
            # Create schema if not already registered
            if func_name not in cls._schemas:
                cls._schemas[func_name] = Tool.create_schema_from_function(target_function)
                logger.debug(f"Created tool schema for: {func_name}, schema: {cls._schemas[func_name]}")
            
            schemas.append(cls._schemas[func_name])
        return schemas

    @classmethod
    def initialize_tools(cls, db: Session):
        """Load tools from database and map to actual functions"""
        default_tools = {
            "search": search,
            "webscraper": webscraper,
            "calculate": calculate
        }
        
        # Get schemas for all tools
        all_schemas = cls.get_or_create_tool_schema(*default_tools.values())
        
        # Update or create tools in database
        for func_name, func in default_tools.items():
            schema = next(s for s in all_schemas if s["name"] == func_name)
            source_code = inspect.getsource(func)
            
            existing_tool = db.query(Tool).filter(
                Tool.name == func_name,
                Tool.is_deleted == False
            ).first()
            
            if existing_tool:
                # Update if source code or schema changed
                if (existing_tool.source_code != source_code or 
                    existing_tool.json_schema != schema):
                    existing_tool.source_code = source_code
                    existing_tool.json_schema = schema
                    existing_tool.description = func.__doc__ or ""
                    db.commit()
            else:
                # Create new tool
                new_tool = Tool(
                    name=func_name,
                    description=func.__doc__ or "",
                    source_type="python",
                    json_schema=schema,
                    source_code=source_code
                )
                db.add(new_tool)
                db.commit()

        # Map functions to tools
        cls._tools = default_tools
        return all_schemas

    @classmethod
    def get_tool(cls, name: str):
        return cls._tools.get(name)

    @classmethod
    def get_available_tools(cls):
        return list(cls._tools.keys())