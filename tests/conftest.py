"""Pytest configuration and fixtures."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from src.todo_txt_mcp.models.config import TodoMCPConfig
from src.todo_txt_mcp.services.todo_service import TodoService


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def test_config(temp_dir: Path) -> TodoMCPConfig:
    """Create a test configuration with temporary files."""
    return TodoMCPConfig(
        todo_file_path=temp_dir / "todo.txt",
        done_file_path=temp_dir / "done.txt",
        backup_enabled=False,  # Disable backups for testing
        auto_archive=False,  # Disable auto-archive for simpler testing
    )


@pytest.fixture
def todo_service(test_config: TodoMCPConfig) -> TodoService:
    """Create a todo service for testing."""
    return TodoService(test_config)


@pytest.fixture
def sample_todo_file(test_config: TodoMCPConfig) -> Path:
    """Create a sample todo.txt file for testing."""
    todo_file = test_config.todo_file_path

    # Create sample todo content
    content = """(A) Call Mom +family @phone
x 2024-01-15 2024-01-10 (B) Buy groceries +shopping @errands
Write project proposal +work @computer
(C) Schedule dentist appointment +health @phone
x 2024-01-14 Clean garage +home @weekend"""

    todo_file.write_text(content, encoding="utf-8")
    return todo_file
