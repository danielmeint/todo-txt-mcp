"""Configuration models for the todo.txt MCP server."""

import os
import re
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class TodoMCPConfig(BaseSettings):
    """Configuration for the todo.txt MCP server."""

    # File paths
    todo_file_path: Path = Field(
        default=Path("todo.txt"), description="Path to the todo.txt file"
    )
    done_file_path: Path | None = Field(
        default=None, description="Path to the done.txt file (optional)"
    )

    # File handling
    encoding: str = Field(
        default="utf-8", description="File encoding for todo.txt files"
    )
    auto_archive: bool = Field(
        default=True, description="Automatically move completed todos to done.txt"
    )
    backup_enabled: bool = Field(default=True, description="Enable automatic backups")
    backup_count: int = Field(default=5, description="Number of backup files to keep")

    # Performance and safety
    max_file_size: int = Field(
        default=10_000_000, description="Maximum file size in bytes"  # 10MB
    )

    class Config:
        env_prefix = "TODO_MCP_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra environment variables

    def get_done_file_path(self) -> Path:
        """Get the done.txt file path, defaulting to same directory as todo.txt."""
        if self.done_file_path:
            return self.done_file_path
        return self.todo_file_path.parent / "done.txt"

    @classmethod
    def from_todo_sh_config(cls, config_path: Path | None = None) -> "TodoMCPConfig":
        """
        Create configuration from a todo.sh config file.

        Args:
            config_path: Path to the todo.sh config file. If None, will search standard locations.

        Returns:
            TodoMCPConfig instance with settings from todo.sh config
        """
        if config_path is None:
            config_path = cls._find_todo_sh_config()

        if config_path is None or not config_path.exists():
            raise ValueError(f"Todo.sh config file not found at {config_path}")

        # Parse the shell config file to extract variables
        variables = cls._parse_shell_config(config_path)

        # Extract relevant paths
        todo_dir = variables.get("TODO_DIR")
        todo_file = variables.get("TODO_FILE")
        done_file = variables.get("DONE_FILE")

        # Resolve paths
        if todo_file:
            todo_file_path = Path(todo_file).expanduser()
        elif todo_dir:
            todo_file_path = Path(todo_dir).expanduser() / "todo.txt"
        else:
            todo_file_path = Path("todo.txt")

        done_file_path = None
        if done_file:
            done_file_path = Path(done_file).expanduser()
        elif todo_dir:
            done_file_path = Path(todo_dir).expanduser() / "done.txt"

        # Create config with resolved paths
        return cls(todo_file_path=todo_file_path, done_file_path=done_file_path)

    @staticmethod
    def _find_todo_sh_config() -> Path | None:
        """Find todo.sh config file in standard locations."""
        standard_locations = [
            Path.home() / ".todo" / "config",
            Path.home() / ".todo.cfg",
            Path("/etc/todo/config"),
            Path("/usr/local/etc/todo/config"),
        ]

        for location in standard_locations:
            if location.exists():
                return location

        return None

    @staticmethod
    def _parse_shell_config(config_path: Path) -> dict[str, str]:
        """
        Parse a shell config file to extract environment variables.

        This is a simple parser that handles basic export statements.
        It doesn't handle complex shell logic, but covers the common todo.sh config patterns.
        """
        variables: dict[str, str] = {}

        try:
            content = config_path.read_text(encoding="utf-8")

            # Pattern to match export statements like: export VAR="value" or export VAR=value
            # Also match simple assignments like: VAR="value" or VAR=value
            export_pattern = re.compile(r"^\s*(?:export\s+)?(\w+)=(.+)$", re.MULTILINE)

            for match in export_pattern.finditer(content):
                var_name = match.group(1)
                var_value = match.group(2).strip()

                # Remove quotes if present
                if var_value.startswith('"') and var_value.endswith('"'):
                    var_value = var_value[1:-1]
                elif var_value.startswith("'") and var_value.endswith("'"):
                    var_value = var_value[1:-1]

                # Handle variable expansion like $HOME, $TODO_DIR
                var_value = TodoMCPConfig._expand_variables(var_value, variables)

                variables[var_name] = var_value

        except Exception as e:
            raise ValueError(
                f"Failed to parse todo.sh config file {config_path}: {e}"
            ) from e

        return variables

    @staticmethod
    def _expand_variables(value: str, variables: dict[str, str]) -> str:
        """Expand shell variables in a value string."""

        # Handle $VAR and ${VAR} patterns
        def replace_var(match: Any) -> str:
            var_name = match.group(1) or match.group(2)

            # Check our parsed variables first
            if var_name in variables:
                return variables[var_name]

            # Fall back to environment variables
            return os.environ.get(var_name, match.group(0))

        # Pattern for $VAR or ${VAR}
        var_pattern = re.compile(r"\$\{(\w+)\}|\$(\w+)")
        expanded = var_pattern.sub(replace_var, value)

        # Handle tilde expansion for home directory
        if expanded.startswith("~"):
            expanded = str(Path(expanded).expanduser())

        return expanded
