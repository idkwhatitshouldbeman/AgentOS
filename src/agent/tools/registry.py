"""
Tool Registry.
Manages available tools and their permissions.
"""

import inspect
import json
from typing import Any, Callable, Dict, List, Optional, get_type_hints

from ..types import ToolDefinition


class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        self.schema = self._generate_schema()

    def _generate_schema(self) -> Dict[str, Any]:
        """Generate JSON Schema from function signature."""
        sig = inspect.signature(self.func)
        type_hints = get_type_hints(self.func)
        
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
                
            param_type = type_hints.get(param_name, str)
            param_desc = "Parameter" # Could parse docstring here later
            
            # Basic type mapping
            json_type = "string"
            if param_type == int:
                json_type = "integer"
            elif param_type == float:
                json_type = "number"
            elif param_type == bool:
                json_type = "boolean"
            elif param_type == list:
                json_type = "array"
            elif param_type == dict:
                json_type = "object"
                
            parameters["properties"][param_name] = {
                "type": json_type,
                "description": param_desc
            }
            
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(param_name)
                
        return {
            "name": self.name,
            "description": self.description,
            "parameters": parameters
        }

    def __call__(self, **kwargs) -> Any:
        return self.func(**kwargs)


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        
    def register(self, tool: Tool):
        """Register a tool instance."""
        self._tools[tool.name] = tool
        
    def register_function(self, name: str, description: str):
        """Decorator to register a function as a tool."""
        def decorator(func: Callable):
            tool = Tool(name, func, description)
            self.register(tool)
            return func
        return decorator
        
    def get_tool(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)
        
    def get_definitions(self) -> List[ToolDefinition]:
        """Get list of tool definitions for the LLM."""
        return [
            ToolDefinition(
                name=t.name,
                description=t.description,
                parameters=t.schema["parameters"]
            )
            for t in self._tools.values()
        ]
