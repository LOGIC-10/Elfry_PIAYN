import inspect
import logging
from typing import Callable, List, Dict
from sqlalchemy.orm import Session
from fastapi.routing import APIRoute
from ..db.database import Tool as DBTool  # 明确指定数据库Tool的别名
from ..api.tools import router as tools_router
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..db.database import Base
from .tool_schema import ToolSchema  # 改为导入ToolSchema

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
    def initialize_tools(cls, db: Session):
        """Load tools from FastAPI endpoints and store in database"""
        # Get all tool endpoints from the router
        tool_routes = [
            route for route in tools_router.routes
            if isinstance(route, APIRoute)
        ]
        
        for route in tool_routes:
            tool_name = route.endpoint.__name__
            schema = ToolSchema.create_schema_from_function(route.endpoint)  # 使用新的类名
            print(schema)
            source_code = inspect.getsource(route.endpoint)
            
            existing_tool = db.query(DBTool).filter(
                DBTool.name == tool_name,
                DBTool.is_deleted == False
            ).first()
            
            if existing_tool: 
                if (existing_tool.source_code != source_code or 
                    existing_tool.json_schema != schema): # 如果数据库中的工具和代码中现在的工具不一致，说明工具有更新，对应的也要更新数据库
                    existing_tool.source_code = source_code
                    existing_tool.json_schema = schema
                    existing_tool.description = schema["function"]["description"]
                    db.commit()
            else: # 如果数据库中没有这个工具，说明是新工具，需要添加到数据库
                new_tool = DBTool(
                    name=tool_name,
                    description=schema["function"]["description"],
                    source_type="python",
                    json_schema=schema,
                    source_code=source_code
                )
                db.add(new_tool)
                db.commit()

            # Store route endpoint for function calls
            # TODO 这两行代码的作用和可用性还需要验证
                # schema要求的是名字和json的对应即可
                # 工具调用里重要的是如何根据名字和schema来现在的api端口
            cls._tools[tool_name] = route.endpoint
            cls._schemas[tool_name] = schema

    @classmethod
    def get_tool(cls, name: str):
        """Get tool by name"""
        return cls._tools.get(name)

    @classmethod
    def get_schema(cls, name: str) -> Dict:
        """Get schema by tool name"""
        return cls._schemas.get(name)

    @classmethod
    def get_available_tools(cls):
        """Get list of available tool names"""
        return list(cls._tools.keys())

    @classmethod
    def get_all_schemas(cls) -> List[Dict]:
        """Get all tool schemas"""
        # 直接返回已经格式化好的 schema 列表
        return list(cls._schemas.values())
