"""MCP tools for CRUD operations on todos."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..services.todo_service import TodoService


def register_crud_tools(mcp: FastMCP, todo_service: TodoService) -> None:
    """Register CRUD tools with the MCP server."""

    @mcp.tool()
    def add_todo(
        text: str,
        priority: str | None = None,
        projects: list[str] | None = None,
        contexts: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Add a new todo item.

        Args:
            text: The todo description text
            priority: Priority level (A-Z), optional
            projects: List of project names (without + prefix), optional
            contexts: List of context names (without @ prefix), optional

        Returns:
            Dictionary containing the created todo details
        """
        try:
            # Strip newlines to prevent corrupting todo.txt file structure
            text = text.replace("\n", " ").replace("\r", " ").strip()

            # Convert lists to sets
            project_set = set(projects) if projects else None
            context_set = set(contexts) if contexts else None

            # Validate priority
            if priority and (
                len(priority) != 1 or not priority.isalpha() or not priority.isupper()
            ):
                return {
                    "error": "Priority must be a single uppercase letter (A-Z)",
                    "priority": priority,
                }

            new_todo = todo_service.add_todo(
                text=text, priority=priority, projects=project_set, contexts=context_set
            )

            return {
                "success": True,
                "todo": {
                    "id": new_todo.id,
                    "text": new_todo.text,
                    "completed": new_todo.completed,
                    "priority": new_todo.priority,
                    "creation_date": (
                        new_todo.creation_date.isoformat()
                        if new_todo.creation_date
                        else None
                    ),
                    "completion_date": (
                        new_todo.completion_date.isoformat()
                        if new_todo.completion_date
                        else None
                    ),
                    "projects": sorted(new_todo.projects),
                    "contexts": sorted(new_todo.contexts),
                    "todo_txt_line": new_todo.to_todo_txt_line(),
                },
                "message": f"Todo added successfully with ID: {new_todo.id}",
            }

        except Exception as e:
            return {"error": f"Failed to add todo: {str(e)}", "text": text}

    @mcp.tool()
    def complete_todo(todo_id: str) -> dict[str, Any]:
        """
        Mark a todo as completed.

        Args:
            todo_id: The unique identifier of the todo to complete

        Returns:
            Dictionary containing success status and message
        """
        success = todo_service.complete_todo(todo_id)

        if success:
            # Get the updated todo to return details
            todo = todo_service.get_todo(todo_id)
            return {
                "success": True,
                "todo_id": todo_id,
                "message": "Todo marked as completed",
                "todo": (
                    {
                        "id": todo.id,
                        "text": todo.text,
                        "completed": todo.completed,
                        "completion_date": (
                            todo.completion_date.isoformat()
                            if todo.completion_date
                            else None
                        ),
                        "todo_txt_line": todo.to_todo_txt_line(),
                    }
                    if todo
                    else None
                ),
            }
        else:
            return {"error": f"Todo with ID '{todo_id}' not found", "todo_id": todo_id}

    @mcp.tool()
    def update_todo(
        todo_id: str,
        text: str | None = None,
        priority: str | None = None,
        projects: list[str] | None = None,
        contexts: list[str] | None = None,
        completed: bool | None = None,
    ) -> dict[str, Any]:
        """
        Update a todo item.

        Args:
            todo_id: The unique identifier of the todo to update
            text: New todo description text, optional
            priority: New priority level (A-Z), optional
            projects: New list of project names (without + prefix), optional
            contexts: New list of context names (without @ prefix), optional
            completed: New completion status, optional

        Returns:
            Dictionary containing success status and updated todo details
        """
        try:
            # Strip newlines from text to prevent corrupting todo.txt file structure
            if text is not None:
                text = text.replace("\n", " ").replace("\r", " ").strip()

            # Validate priority if provided
            if priority and (
                len(priority) != 1 or not priority.isalpha() or not priority.isupper()
            ):
                return {
                    "error": "Priority must be a single uppercase letter (A-Z)",
                    "priority": priority,
                    "todo_id": todo_id,
                }

            # Convert lists to sets
            project_set = set(projects) if projects is not None else None
            context_set = set(contexts) if contexts is not None else None

            success = todo_service.update_todo(
                todo_id=todo_id,
                text=text,
                priority=priority,
                projects=project_set,
                contexts=context_set,
                completed=completed,
            )

            if success:
                # Get the updated todo to return details
                todo = todo_service.get_todo(todo_id)
                return {
                    "success": True,
                    "todo_id": todo_id,
                    "message": "Todo updated successfully",
                    "todo": (
                        {
                            "id": todo.id,
                            "text": todo.text,
                            "completed": todo.completed,
                            "priority": todo.priority,
                            "creation_date": (
                                todo.creation_date.isoformat()
                                if todo.creation_date
                                else None
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
                        if todo
                        else None
                    ),
                }
            else:
                return {
                    "error": f"Todo with ID '{todo_id}' not found",
                    "todo_id": todo_id,
                }

        except Exception as e:
            return {"error": f"Failed to update todo: {str(e)}", "todo_id": todo_id}

    @mcp.tool()
    def delete_todo(todo_id: str) -> dict[str, Any]:
        """
        Delete a todo item.

        Args:
            todo_id: The unique identifier of the todo to delete

        Returns:
            Dictionary containing success status and message
        """
        # Get the todo details before deletion for confirmation
        todo = todo_service.get_todo(todo_id)

        success = todo_service.delete_todo(todo_id)

        if success:
            return {
                "success": True,
                "todo_id": todo_id,
                "message": "Todo deleted successfully",
                "deleted_todo": (
                    {"text": todo.text, "todo_txt_line": todo.to_todo_txt_line()}
                    if todo
                    else None
                ),
            }
        else:
            return {"error": f"Todo with ID '{todo_id}' not found", "todo_id": todo_id}

    @mcp.tool()
    def reload_todos() -> dict[str, Any]:
        """
        Reload todos from the file system.

        This is useful if the todo.txt file has been modified externally.

        Returns:
            Dictionary containing success status and current todo count
        """
        try:
            todo_service.reload_from_file()
            todos = todo_service.list_todos(include_completed=True)

            return {
                "success": True,
                "message": "Todos reloaded from file",
                "total_todos": len(todos),
            }

        except Exception as e:
            return {"error": f"Failed to reload todos: {str(e)}"}
