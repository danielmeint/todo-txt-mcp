"""Todo.txt MCP Server - A minimal but extensible MCP server for todo.txt files."""

__version__ = "0.1.0"
__author__ = "Todo.txt MCP Team"
__description__ = "Model Context Protocol server for todo.txt file management"

from .server import create_server

__all__ = ["create_server"]
