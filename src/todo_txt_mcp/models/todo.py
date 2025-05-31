"""Todo item and list models."""

from datetime import date
from uuid import uuid4

import pytodotxt
from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    """A todo item with MCP-friendly interface."""

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique identifier"
    )
    text: str = Field(description="The full todo text")
    completed: bool = Field(default=False, description="Whether the todo is completed")
    priority: str | None = Field(default=None, description="Priority level (A-Z)")
    creation_date: date | None = Field(
        default=None, description="Date when todo was created"
    )
    completion_date: date | None = Field(
        default=None, description="Date when todo was completed"
    )
    projects: set[str] = Field(default_factory=set, description="Projects (+project)")
    contexts: set[str] = Field(default_factory=set, description="Contexts (@context)")

    @classmethod
    def from_pytodotxt_task(
        cls, task: pytodotxt.Task, task_id: str | None = None
    ) -> "TodoItem":
        """Create a TodoItem from a pytodotxt Task."""
        return cls(
            id=task_id or str(uuid4()),
            text=task.description,
            completed=task.is_completed,
            priority=task.priority,
            creation_date=task.creation_date,
            completion_date=task.completion_date,
            projects=set(task.projects or []),
            contexts=set(task.contexts or []),
        )

    def to_todo_txt_line(self) -> str:
        """Convert to a todo.txt format line."""
        parts = []

        # Add completion marker
        if self.completed:
            parts.append("x")
            if self.completion_date:
                parts.append(self.completion_date.strftime("%Y-%m-%d"))

        # Add priority (only for non-completed todos)
        if self.priority and not self.completed:
            parts.append(f"({self.priority})")

        # Add creation date
        if self.creation_date:
            parts.append(self.creation_date.strftime("%Y-%m-%d"))

        # Add the main text
        parts.append(self.text)

        # Add projects
        for project in sorted(self.projects):
            parts.append(f"+{project}")

        # Add contexts
        for context in sorted(self.contexts):
            parts.append(f"@{context}")

        return " ".join(parts)


class TodoList(BaseModel):
    """A collection of todo items."""

    items: list[TodoItem] = Field(
        default_factory=list, description="List of todo items"
    )

    @classmethod
    def from_pytodotxt_list(cls, todo_list: pytodotxt.TodoTxt) -> "TodoList":
        """Create a TodoList from a pytodotxt TodoTxt object."""
        items = []
        for i, task in enumerate(todo_list.tasks):
            # Use index as a simple ID for now
            task_id = str(i)
            items.append(TodoItem.from_pytodotxt_task(task, task_id))
        return cls(items=items)

    def to_todo_txt_content(self) -> str:
        """Convert to todo.txt file content."""
        lines = []
        for item in self.items:
            lines.append(item.to_todo_txt_line())
        return "\n".join(lines)

    def get_by_id(self, todo_id: str) -> TodoItem | None:
        """Get a todo item by ID."""
        for item in self.items:
            if item.id == todo_id:
                return item
        return None

    def add_item(self, item: TodoItem) -> None:
        """Add a todo item to the list."""
        self.items.append(item)

    def remove_item(self, todo_id: str) -> bool:
        """Remove a todo item by ID. Returns True if removed, False if not found."""
        for i, item in enumerate(self.items):
            if item.id == todo_id:
                del self.items[i]
                return True
        return False

    def get_active_items(self) -> list[TodoItem]:
        """Get all non-completed todo items."""
        return [item for item in self.items if not item.completed]

    def get_completed_items(self) -> list[TodoItem]:
        """Get all completed todo items."""
        return [item for item in self.items if item.completed]

    def get_by_priority(self, priority: str) -> list[TodoItem]:
        """Get all items with a specific priority."""
        return [item for item in self.items if item.priority == priority]

    def get_by_project(self, project: str) -> list[TodoItem]:
        """Get all items containing a specific project."""
        return [item for item in self.items if project in item.projects]

    def get_by_context(self, context: str) -> list[TodoItem]:
        """Get all items containing a specific context."""
        return [item for item in self.items if context in item.contexts]
