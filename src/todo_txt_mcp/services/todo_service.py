"""Todo service for business logic operations."""

from datetime import date
from typing import Any

from ..models.config import TodoMCPConfig
from ..models.todo import TodoItem, TodoList
from .file_service import FileService


class TodoService:
    """Service for todo business logic operations."""

    def __init__(self, config: TodoMCPConfig):
        self.config = config
        self.file_service = FileService(config)
        self._todo_list: TodoList | None = None

    def _get_todo_list(self) -> TodoList:
        """Get the current todo list, loading from file if necessary."""
        if self._todo_list is None:
            self._todo_list = self.file_service.load_todo_list()
        return self._todo_list

    def _save_todo_list(self) -> None:
        """Save the current todo list to file."""
        if self._todo_list is not None:
            self.file_service.save_todo_list(self._todo_list)

    def reload_from_file(self) -> None:
        """Force reload the todo list from file."""
        self._todo_list = None

    def list_todos(self, include_completed: bool = False) -> list[TodoItem]:
        """List all todos, optionally including completed ones."""
        todo_list = self._get_todo_list()

        if include_completed:
            return todo_list.items
        else:
            return todo_list.get_active_items()

    def get_todo(self, todo_id: str) -> TodoItem | None:
        """Get a specific todo by ID."""
        todo_list = self._get_todo_list()
        return todo_list.get_by_id(todo_id)

    def add_todo(
        self,
        text: str,
        priority: str | None = None,
        projects: set[str] | None = None,
        contexts: set[str] | None = None,
        creation_date: date | None = None,
    ) -> TodoItem:
        """Add a new todo item."""
        todo_list = self._get_todo_list()

        # Create the new todo item
        new_todo = TodoItem(
            text=text,
            priority=priority,
            projects=projects or set(),
            contexts=contexts or set(),
            creation_date=creation_date or date.today(),
        )

        # Add to list and save
        todo_list.add_item(new_todo)
        self._save_todo_list()

        return new_todo

    def complete_todo(self, todo_id: str) -> bool:
        """Mark a todo as completed."""
        todo_list = self._get_todo_list()
        todo_item = todo_list.get_by_id(todo_id)

        if todo_item is None:
            return False

        # Mark as completed
        todo_item.completed = True
        todo_item.completion_date = date.today()

        # Save changes
        self._save_todo_list()
        return True

    def update_todo(
        self,
        todo_id: str,
        text: str | None = None,
        priority: str | None = None,
        projects: set[str] | None = None,
        contexts: set[str] | None = None,
        completed: bool | None = None,
    ) -> bool:
        """Update a todo item."""
        todo_list = self._get_todo_list()
        todo_item = todo_list.get_by_id(todo_id)

        if todo_item is None:
            return False

        # Update fields if provided
        if text is not None:
            todo_item.text = text
        if priority is not None:
            todo_item.priority = priority
        if projects is not None:
            todo_item.projects = projects
        if contexts is not None:
            todo_item.contexts = contexts
        if completed is not None:
            todo_item.completed = completed
            if completed:
                todo_item.completion_date = date.today()
            else:
                todo_item.completion_date = None

        # Save changes
        self._save_todo_list()
        return True

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item."""
        todo_list = self._get_todo_list()
        removed = todo_list.remove_item(todo_id)

        if removed:
            self._save_todo_list()

        return removed

    def search_todos(
        self, query: str, include_completed: bool = False
    ) -> list[TodoItem]:
        """Search todos by text content."""
        todos = self.list_todos(include_completed=include_completed)
        query_lower = query.lower()

        return [todo for todo in todos if query_lower in todo.text.lower()]

    def filter_by_priority(
        self, priority: str, include_completed: bool = False
    ) -> list[TodoItem]:
        """Filter todos by priority."""
        todos = self.list_todos(include_completed=include_completed)
        return [todo for todo in todos if todo.priority == priority]

    def filter_by_project(
        self, project: str, include_completed: bool = False
    ) -> list[TodoItem]:
        """Filter todos by project."""
        todos = self.list_todos(include_completed=include_completed)
        return [todo for todo in todos if project in todo.projects]

    def filter_by_context(
        self, context: str, include_completed: bool = False
    ) -> list[TodoItem]:
        """Filter todos by context."""
        todos = self.list_todos(include_completed=include_completed)
        return [todo for todo in todos if context in todo.contexts]

    def get_statistics(self) -> dict[str, Any]:
        """Get statistics about the todo list."""
        todo_list = self._get_todo_list()
        active_items = todo_list.get_active_items()
        completed_items = todo_list.get_completed_items()

        # Count by priority
        priority_counts: dict[str, int] = {}
        for item in active_items:
            priority = item.priority or "None"
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

        # Get all projects and contexts
        all_projects = set()
        all_contexts = set()
        for item in active_items:
            all_projects.update(item.projects)
            all_contexts.update(item.contexts)

        # File stats
        file_stats = self.file_service.get_file_stats()

        return {
            "total_todos": len(todo_list.items),
            "active_todos": len(active_items),
            "completed_todos": len(completed_items),
            "priority_counts": priority_counts,
            "projects": sorted(all_projects),
            "contexts": sorted(all_contexts),
            "file_stats": file_stats,
        }

    def get_done_todos(self) -> list[TodoItem]:
        """Get completed todos from done.txt file."""
        done_list = self.file_service.load_done_list()
        return done_list.items if done_list else []
