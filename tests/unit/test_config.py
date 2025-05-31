"""Unit tests for TodoMCPConfig, including todo.sh config support."""

import tempfile
from pathlib import Path

import pytest

from src.todo_txt_mcp.models.config import TodoMCPConfig


def test_default_config():
    """Test default configuration."""
    config = TodoMCPConfig()

    assert config.todo_file_path == Path("todo.txt")
    assert config.encoding == "utf-8"
    assert config.auto_archive is True
    assert config.backup_enabled is True


def test_get_done_file_path():
    """Test done file path resolution."""
    config = TodoMCPConfig(todo_file_path=Path("/home/user/todos/todo.txt"))

    # Should default to same directory as todo.txt
    assert config.get_done_file_path() == Path("/home/user/todos/done.txt")

    # Should use explicit done file path if provided
    config.done_file_path = Path("/home/user/archive/done.txt")
    assert config.get_done_file_path() == Path("/home/user/archive/done.txt")


def test_from_todo_sh_config_basic():
    """Test loading from a basic todo.sh config file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config"

        # Create a sample todo.sh config
        config_content = """
# Sample todo.sh config
export TODO_DIR="/home/user/Dropbox/todo"
export TODO_FILE="$TODO_DIR/todo.txt"
export DONE_FILE="$TODO_DIR/done.txt"
export REPORT_FILE="$TODO_DIR/report.txt"
"""
        config_path.write_text(config_content)

        # Load config
        config = TodoMCPConfig.from_todo_sh_config(config_path)

        assert config.todo_file_path == Path("/home/user/Dropbox/todo/todo.txt")
        assert config.done_file_path == Path("/home/user/Dropbox/todo/done.txt")


def test_from_todo_sh_config_with_quotes():
    """Test loading from todo.sh config with quoted values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config"

        # Create config with various quote styles
        config_content = """
export TODO_DIR="/Users/alice/Documents/todo-txt"
export TODO_FILE='$TODO_DIR/my-todo.txt'
export DONE_FILE="$TODO_DIR/my-done.txt"
"""
        config_path.write_text(config_content)

        # Load config
        config = TodoMCPConfig.from_todo_sh_config(config_path)

        assert config.todo_file_path == Path(
            "/Users/alice/Documents/todo-txt/my-todo.txt"
        )
        assert config.done_file_path == Path(
            "/Users/alice/Documents/todo-txt/my-done.txt"
        )


def test_from_todo_sh_config_todo_dir_only():
    """Test loading when only TODO_DIR is specified."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config"

        config_content = """
export TODO_DIR="/Users/bob/todo"
"""
        config_path.write_text(config_content)

        # Load config
        config = TodoMCPConfig.from_todo_sh_config(config_path)

        assert config.todo_file_path == Path("/Users/bob/todo/todo.txt")
        assert config.done_file_path == Path("/Users/bob/todo/done.txt")


def test_from_todo_sh_config_absolute_paths():
    """Test loading with absolute file paths."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config"

        config_content = """
export TODO_FILE="/absolute/path/to/my-todos.txt"
export DONE_FILE="/different/path/completed.txt"
"""
        config_path.write_text(config_content)

        # Load config
        config = TodoMCPConfig.from_todo_sh_config(config_path)

        assert config.todo_file_path == Path("/absolute/path/to/my-todos.txt")
        assert config.done_file_path == Path("/different/path/completed.txt")


def test_from_todo_sh_config_variable_expansion():
    """Test variable expansion in config values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config"

        config_content = """
export BASE_DIR="/home/charlie"
export TODO_DIR="$BASE_DIR/todo-txt"
export TODO_FILE="${TODO_DIR}/todo.txt"
"""
        config_path.write_text(config_content)

        # Load config
        config = TodoMCPConfig.from_todo_sh_config(config_path)

        assert config.todo_file_path == Path("/home/charlie/todo-txt/todo.txt")


def test_from_todo_sh_config_nonexistent_file():
    """Test error handling for nonexistent config file."""
    with pytest.raises(ValueError, match="Todo.sh config file not found"):
        TodoMCPConfig.from_todo_sh_config(Path("/nonexistent/config"))


def test_parse_shell_config_malformed():
    """Test handling of malformed config file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config"

        # Create malformed config (should still work, just skip bad lines)
        config_content = """
export TODO_DIR="/valid/path"
this is not a valid export line
export TODO_FILE="$TODO_DIR/todo.txt"
# This is a comment and should be ignored
"""
        config_path.write_text(config_content)

        # Should still work and extract valid exports
        config = TodoMCPConfig.from_todo_sh_config(config_path)
        assert config.todo_file_path == Path("/valid/path/todo.txt")


def test_from_todo_sh_config_simple_assignments():
    """Test loading from todo.sh config with simple VAR=value assignments (no export)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config"

        config_content = """
TODO_DIR=~/.todo
TODO_FILE=~/.todo/todo.txt
DONE_FILE=~/.todo/done.txt
REPORT_FILE=~/.todo/report.txt
"""
        config_path.write_text(config_content)

        # Load config
        config = TodoMCPConfig.from_todo_sh_config(config_path)

        # Should expand ~ properly
        expected_todo = Path.home() / ".todo" / "todo.txt"
        expected_done = Path.home() / ".todo" / "done.txt"

        assert config.todo_file_path == expected_todo
        assert config.done_file_path == expected_done


def test_find_todo_sh_config(monkeypatch):
    """Test finding todo.sh config in standard locations."""

    # Mock Path.exists to simulate config file locations
    def mock_exists(self):
        return str(self) == str(Path.home() / ".todo.cfg")

    monkeypatch.setattr(Path, "exists", mock_exists)

    found_config = TodoMCPConfig._find_todo_sh_config()
    assert found_config == Path.home() / ".todo.cfg"
