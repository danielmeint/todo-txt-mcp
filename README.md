# Todo.txt MCP Server

[![PyPI version](https://badge.fury.io/py/todo-txt-mcp.svg)](https://badge.fury.io/py/todo-txt-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A [Model Context Protocol](https://modelcontextprotocol.io/) server that connects [todo.txt](http://todotxt.org/) files
to AI assistants like Claude. Manage your tasks through natural language while keeping the simplicity and portability of
plain text.

## Installation

```bash
# Recommended
uv tool install todo-txt-mcp

# Or run directly without installing
uvx todo-txt-mcp

# Alternatives
pipx install todo-txt-mcp
pip install todo-txt-mcp
```

## Configuration

Add to your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
    "mcpServers": {
        "todo-txt": {
            "command": "uvx",
            "args": [
                "todo-txt-mcp"
            ]
        }
    }
}
```

Restart Claude Desktop. The tools icon confirms the server is connected.

### Custom todo.txt location

```json
{
    "mcpServers": {
        "todo-txt": {
            "command": "uvx",
            "args": [
                "todo-txt-mcp",
                "/path/to/your/todo.txt"
            ]
        }
    }
}
```

### todo.sh integration

If you use [todo.sh](https://github.com/todotxt/todo.txt-cli), the server automatically detects your config from
`~/.todo/config`, `~/.todo.cfg`, or standard system locations.

### Environment variables

```bash
TODO_MCP_TODO_FILE_PATH=/path/to/todo.txt
TODO_MCP_BACKUP_ENABLED=true
TODO_MCP_MAX_FILE_SIZE=10000000
```

## Available Tools

| Tool                 | Description                      |
|----------------------|----------------------------------|
| `list_todos`         | List todos with optional filters |
| `add_todo`           | Create new todos                 |
| `complete_todo`      | Mark todos as completed          |
| `update_todo`        | Modify existing todos            |
| `delete_todo`        | Remove todos                     |
| `search_todos`       | Find todos by text               |
| `filter_by_priority` | Filter by priority (A-Z)         |
| `filter_by_project`  | Filter by project (+tag)         |
| `filter_by_context`  | Filter by context (@tag)         |
| `get_statistics`     | Get todo statistics              |

## Todo.txt Format

Fully compatible with the [todo.txt specification](http://todotxt.org/):

```
(A) Call Mom +family @phone
x 2025-05-31 2025-05-30 (B) Buy groceries +shopping @errands
Write project proposal +work @computer
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Bug reports and feature requests welcome
via [GitHub Issues](https://github.com/danielmeint/todo-txt-mcp/issues).

## License

MIT - see [LICENSE](LICENSE).
