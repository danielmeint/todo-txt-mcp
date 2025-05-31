"""MCP tools for listing and querying todos."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..services.todo_service import TodoService


def register_list_tools(mcp: FastMCP, todo_service: TodoService) -> None:
    """Register list and query tools with the MCP server."""

    @mcp.tool()
    def list_todos(include_completed: bool = False) -> dict[str, Any]:
        """
        List all todos, optionally including completed ones.

        Args:
            include_completed: Whether to include completed todos in the list

        Returns:
            Dictionary containing the list of todos and summary information
        """
        todos = todo_service.list_todos(include_completed=include_completed)

        return {
            "todos": [
                {
                    "id": todo.id,
                    "text": todo.text,
                    "completed": todo.completed,
                    "priority": todo.priority,
                    "creation_date": (
                        todo.creation_date.isoformat() if todo.creation_date else None
                    ),
                    "completion_date": (
                        todo.completion_date.isoformat()
                        if todo.completion_date
                        else None
                    ),
                    "projects": sorted(todo.projects),
                    "contexts": sorted(todo.contexts),
                    "todo_txt_line": todo.to_todo_txt_line(),
                }
                for todo in todos
            ],
            "count": len(todos),
            "include_completed": include_completed,
        }

    @mcp.tool()
    def get_todo(todo_id: str) -> dict[str, Any]:
        """
        Get a specific todo by its ID.

        Args:
            todo_id: The unique identifier of the todo

        Returns:
            Dictionary containing the todo details or error message
        """
        todo = todo_service.get_todo(todo_id)

        if todo is None:
            return {"error": f"Todo with ID '{todo_id}' not found", "todo_id": todo_id}

        return {
            "todo": {
                "id": todo.id,
                "text": todo.text,
                "completed": todo.completed,
                "priority": todo.priority,
                "creation_date": (
                    todo.creation_date.isoformat() if todo.creation_date else None
                ),
                "completion_date": (
                    todo.completion_date.isoformat() if todo.completion_date else None
                ),
                "projects": sorted(todo.projects),
                "contexts": sorted(todo.contexts),
                "todo_txt_line": todo.to_todo_txt_line(),
            }
        }

    @mcp.tool()
    def search_todos(query: str, include_completed: bool = False) -> dict[str, Any]:
        """
        Search todos by text content.

        Args:
            query: Text to search for in todo descriptions
            include_completed: Whether to include completed todos in search

        Returns:
            Dictionary containing matching todos and search information
        """
        todos = todo_service.search_todos(query, include_completed=include_completed)

        return {
            "todos": [
                {
                    "id": todo.id,
                    "text": todo.text,
                    "completed": todo.completed,
                    "priority": todo.priority,
                    "creation_date": (
                        todo.creation_date.isoformat() if todo.creation_date else None
                    ),
                    "completion_date": (
                        todo.completion_date.isoformat()
                        if todo.completion_date
                        else None
                    ),
                    "projects": sorted(todo.projects),
                    "contexts": sorted(todo.contexts),
                    "todo_txt_line": todo.to_todo_txt_line(),
                }
                for todo in todos
            ],
            "count": len(todos),
            "query": query,
            "include_completed": include_completed,
        }

    @mcp.tool()
    def filter_by_priority(
        priority: str, include_completed: bool = False
    ) -> dict[str, Any]:
        """
        Filter todos by priority level.

        Args:
            priority: Priority level (A-Z)
            include_completed: Whether to include completed todos

        Returns:
            Dictionary containing filtered todos
        """
        todos = todo_service.filter_by_priority(
            priority, include_completed=include_completed
        )

        return {
            "todos": [
                {
                    "id": todo.id,
                    "text": todo.text,
                    "completed": todo.completed,
                    "priority": todo.priority,
                    "creation_date": (
                        todo.creation_date.isoformat() if todo.creation_date else None
                    ),
                    "completion_date": (
                        todo.completion_date.isoformat()
                        if todo.completion_date
                        else None
                    ),
                    "projects": sorted(todo.projects),
                    "contexts": sorted(todo.contexts),
                    "todo_txt_line": todo.to_todo_txt_line(),
                }
                for todo in todos
            ],
            "count": len(todos),
            "priority": priority,
            "include_completed": include_completed,
        }

    @mcp.tool()
    def filter_by_project(
        project: str, include_completed: bool = False
    ) -> dict[str, Any]:
        """
        Filter todos by project.

        Args:
            project: Project name (without the + prefix)
            include_completed: Whether to include completed todos

        Returns:
            Dictionary containing filtered todos
        """
        todos = todo_service.filter_by_project(
            project, include_completed=include_completed
        )

        return {
            "todos": [
                {
                    "id": todo.id,
                    "text": todo.text,
                    "completed": todo.completed,
                    "priority": todo.priority,
                    "creation_date": (
                        todo.creation_date.isoformat() if todo.creation_date else None
                    ),
                    "completion_date": (
                        todo.completion_date.isoformat()
                        if todo.completion_date
                        else None
                    ),
                    "projects": sorted(todo.projects),
                    "contexts": sorted(todo.contexts),
                    "todo_txt_line": todo.to_todo_txt_line(),
                }
                for todo in todos
            ],
            "count": len(todos),
            "project": project,
            "include_completed": include_completed,
        }

    @mcp.tool()
    def filter_by_context(
        context: str, include_completed: bool = False
    ) -> dict[str, Any]:
        """
        Filter todos by context.

        Args:
            context: Context name (without the @ prefix)
            include_completed: Whether to include completed todos

        Returns:
            Dictionary containing filtered todos
        """
        todos = todo_service.filter_by_context(
            context, include_completed=include_completed
        )

        return {
            "todos": [
                {
                    "id": todo.id,
                    "text": todo.text,
                    "completed": todo.completed,
                    "priority": todo.priority,
                    "creation_date": (
                        todo.creation_date.isoformat() if todo.creation_date else None
                    ),
                    "completion_date": (
                        todo.completion_date.isoformat()
                        if todo.completion_date
                        else None
                    ),
                    "projects": sorted(todo.projects),
                    "contexts": sorted(todo.contexts),
                    "todo_txt_line": todo.to_todo_txt_line(),
                }
                for todo in todos
            ],
            "count": len(todos),
            "context": context,
            "include_completed": include_completed,
        }

    @mcp.tool()
    def get_statistics() -> dict[str, Any]:
        """
        Get statistics about the todo list.

        Returns:
            Dictionary containing various statistics about todos
        """
        return todo_service.get_statistics()
