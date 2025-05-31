"""Main MCP server for todo.txt management."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .models.config import TodoMCPConfig
from .services.todo_service import TodoService
from .tools.crud_tools import register_crud_tools
from .tools.list_tools import register_list_tools


def create_server(
    name: str = "todo-txt-mcp",
    todo_file_path: str | None = None,
    todo_sh_config_path: str | None = None,
    config: TodoMCPConfig | None = None,
) -> FastMCP:
    """
    Create and configure the todo.txt MCP server.

    Args:
        name: Name of the MCP server
        todo_file_path: Path to the todo.txt file (overrides config)
        todo_sh_config_path: Path to the todo.sh config file (alternative to manual config)
        config: Configuration object (optional)

    Returns:
        Configured FastMCP server instance
    """
    # Create or use provided config
    if config is None:
        if todo_sh_config_path:
            # Load from todo.sh config file
            config_path = (
                Path(todo_sh_config_path) if todo_sh_config_path != "auto" else None
            )
            config = TodoMCPConfig.from_todo_sh_config(config_path)
        else:
            # Try to auto-detect todo.sh config, fall back to default
            try:
                config = TodoMCPConfig.from_todo_sh_config()
            except ValueError:
                # No todo.sh config found, use default
                config = TodoMCPConfig()

    # Override todo file path if provided
    if todo_file_path:
        config.todo_file_path = Path(todo_file_path)

    # Create the FastMCP server
    mcp = FastMCP(name)

    # Create the todo service
    todo_service = TodoService(config)

    # Register all tools
    register_list_tools(mcp, todo_service)
    register_crud_tools(mcp, todo_service)

    # Add a simple resource for the todo file content
    @mcp.resource("todo://file")
    def get_todo_file() -> str:
        """Get the raw content of the todo.txt file."""
        try:
            if config.todo_file_path.exists():
                return config.todo_file_path.read_text(encoding=config.encoding)
            else:
                return "# Todo.txt file not found or empty"
        except Exception as e:
            return f"# Error reading todo.txt file: {e}"

    @mcp.resource("todo://stats")
    def get_todo_stats() -> str:
        """Get todo statistics as formatted text."""
        try:
            stats = todo_service.get_statistics()

            lines = [
                "# Todo.txt Statistics",
                "",
                f"**Total todos:** {stats['total_todos']}",
                f"**Active todos:** {stats['active_todos']}",
                f"**Completed todos:** {stats['completed_todos']}",
                "",
                "## Priority Distribution",
            ]

            for priority, count in sorted(stats["priority_counts"].items()):
                lines.append(f"- **{priority}:** {count}")

            if stats["projects"]:
                lines.extend(
                    [
                        "",
                        "## Projects",
                    ]
                )
                for project in stats["projects"]:
                    lines.append(f"- +{project}")

            if stats["contexts"]:
                lines.extend(
                    [
                        "",
                        "## Contexts",
                    ]
                )
                for context in stats["contexts"]:
                    lines.append(f"- @{context}")

            lines.extend(
                [
                    "",
                    "## File Information",
                    f"**Todo file:** {stats['file_stats']['todo_file']['path']}",
                    f"**File exists:** {stats['file_stats']['todo_file']['exists']}",
                    f"**File size:** {stats['file_stats']['todo_file']['size']} bytes",
                ]
            )

            return "\n".join(lines)

        except Exception as e:
            return f"# Error getting statistics: {e}"

    return mcp


def main() -> None:
    """Main entry point for running the server."""
    import sys

    # Parse command line arguments
    todo_file_path = None
    todo_sh_config_path = None

    if len(sys.argv) > 1:
        arg = sys.argv[1]

        # Check if it's a todo.sh config file or a todo.txt file
        if (
            arg.endswith((".cfg", "/config"))
            or "todo" in Path(arg).name
            and not arg.endswith(".txt")
        ):
            todo_sh_config_path = arg
        else:
            todo_file_path = arg

    # If no arguments, try to auto-detect todo.sh config
    if not todo_file_path and not todo_sh_config_path:
        todo_sh_config_path = "auto"

    # Create and run the server
    server = create_server(
        todo_file_path=todo_file_path, todo_sh_config_path=todo_sh_config_path
    )
    server.run()


if __name__ == "__main__":
    main()
