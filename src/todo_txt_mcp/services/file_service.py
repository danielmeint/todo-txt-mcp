"""File service for todo.txt file operations."""

import shutil
from pathlib import Path
from typing import Any

import pytodotxt

from ..models.config import TodoMCPConfig
from ..models.todo import TodoList


class FileService:
    """Service for handling todo.txt file operations."""

    def __init__(self, config: TodoMCPConfig):
        self.config = config

    def _ensure_file_exists(self, file_path: Path) -> None:
        """Ensure the file exists, creating it if necessary."""
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()

    def _create_backup(self, file_path: Path) -> None:
        """Create a backup of the file if backup is enabled."""
        if not self.config.backup_enabled or not file_path.exists():
            return

        backup_dir = file_path.parent / ".backups"
        backup_dir.mkdir(exist_ok=True)

        # Create backup with timestamp
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{file_path.name}.{timestamp}.bak"

        shutil.copy2(file_path, backup_path)

        # Clean up old backups
        self._cleanup_old_backups(backup_dir, file_path.name)

    def _cleanup_old_backups(self, backup_dir: Path, filename: str) -> None:
        """Remove old backup files, keeping only the configured number."""
        pattern = f"{filename}.*.bak"
        backups = sorted(
            backup_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True
        )

        # Remove excess backups
        for backup in backups[self.config.backup_count :]:
            backup.unlink()

    def _check_file_size(self, file_path: Path) -> None:
        """Check if file size is within limits."""
        if file_path.exists() and file_path.stat().st_size > self.config.max_file_size:
            raise ValueError(
                f"File {file_path} exceeds maximum size of {self.config.max_file_size} bytes"
            )

    def load_todo_list(self) -> TodoList:
        """Load the todo list from the todo.txt file."""
        todo_path = self.config.todo_file_path
        self._ensure_file_exists(todo_path)
        self._check_file_size(todo_path)

        try:
            # Use pytodotxt to parse the file
            pytodo_list = pytodotxt.TodoTxt(str(todo_path))
            pytodo_list.parse()

            # Convert to our TodoList model
            return TodoList.from_pytodotxt_list(pytodo_list)

        except Exception as e:
            raise ValueError(f"Failed to load todo list from {todo_path}: {e}") from e

    def save_todo_list(self, todo_list: TodoList) -> None:
        """Save the todo list to the todo.txt file."""
        todo_path = self.config.todo_file_path

        # Create backup before saving
        self._create_backup(todo_path)

        try:
            # Convert to todo.txt content and save directly
            content = todo_list.to_todo_txt_content()
            todo_path.write_text(content, encoding=self.config.encoding)

            # Archive completed todos if enabled
            if self.config.auto_archive:
                self._archive_completed_todos(todo_list)

        except Exception as e:
            raise ValueError(f"Failed to save todo list to {todo_path}: {e}") from e

    def _archive_completed_todos(self, todo_list: TodoList) -> None:
        """Move completed todos to done.txt file."""
        completed_items = todo_list.get_completed_items()
        if not completed_items:
            return

        done_path = self.config.get_done_file_path()
        self._ensure_file_exists(done_path)

        try:
            # Load existing done.txt
            done_list = TodoList(items=[])
            if done_path.exists() and done_path.stat().st_size > 0:
                pytodo_done = pytodotxt.TodoTxt(str(done_path))
                pytodo_done.parse()
                done_list = TodoList.from_pytodotxt_list(pytodo_done)

            # Add completed items to done list
            for item in completed_items:
                done_list.add_item(item)

            # Save done.txt
            content = done_list.to_todo_txt_content()
            done_path.write_text(content, encoding=self.config.encoding)

            # Remove completed items from main todo list
            for item in completed_items:
                todo_list.remove_item(item.id)

        except Exception as e:
            # Don't fail the main save operation if archiving fails
            print(f"Warning: Failed to archive completed todos: {e}")

    def load_done_list(self) -> TodoList | None:
        """Load the done list from the done.txt file."""
        done_path = self.config.get_done_file_path()

        if not done_path.exists():
            return None

        self._check_file_size(done_path)

        try:
            pytodo_done = pytodotxt.TodoTxt(str(done_path))
            pytodo_done.parse()
            return TodoList.from_pytodotxt_list(pytodo_done)

        except Exception as e:
            raise ValueError(f"Failed to load done list from {done_path}: {e}") from e

    def get_file_stats(self) -> dict[str, Any]:
        """Get statistics about the todo.txt files."""
        todo_path = self.config.todo_file_path
        done_path = self.config.get_done_file_path()

        stats = {
            "todo_file": {
                "path": str(todo_path),
                "exists": todo_path.exists(),
                "size": todo_path.stat().st_size if todo_path.exists() else 0,
                "modified": todo_path.stat().st_mtime if todo_path.exists() else None,
            },
            "done_file": {
                "path": str(done_path),
                "exists": done_path.exists(),
                "size": done_path.stat().st_size if done_path.exists() else 0,
                "modified": done_path.stat().st_mtime if done_path.exists() else None,
            },
        }

        return stats
