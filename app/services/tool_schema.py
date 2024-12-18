
import inspect
import logging
from typing import Callable, Dict, List
from pydantic import create_model
from typing import get_type_hints

logger = logging.getLogger(__name__)

class ToolSchema:
    @staticmethod
    def create_schema_from_function(func: Callable) -> Dict:
        """Create OpenAI tool schema from function signature"""
        doc = inspect.getdoc(func) or ""
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for name, param in signature.parameters.items():
            if name == 'self':
                continue
                
            param_type = type_hints.get(name, str)
            if param_type == str:
                param_schema = {"type": "string"}
            elif param_type == int:
                param_schema = {"type": "integer"}
            elif param_type == float:
                param_schema = {"type": "number"}
            elif param_type == bool:
                param_schema = {"type": "boolean"}
            else:
                param_schema = {"type": "string"}  # default to string
                
            parameters["properties"][name] = param_schema
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(name)
        
        return {
            "name": func.__name__,
            "description": doc,
            "parameters": parameters
        }