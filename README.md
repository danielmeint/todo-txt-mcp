# Todo.txt MCP Server

[![PyPI version](https://badge.fury.io/py/todo-txt-mcp.svg)](https://badge.fury.io/py/todo-txt-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Model Context Protocol (MCP) server that connects your [todo.txt](http://todotxt.org/) files to AI assistants like Claude Desktop. Manage your todo list through natural language while maintaining the simplicity and portability of the todo.txt format.

## ✨ Features

- **🔍 Natural Language Interface**: Ask AI to find, create, and manage your todos
- **📝 Full CRUD Operations**: Create, read, update, and delete todos with AI assistance
- **🎯 Smart Filtering**: Search by text, priority, projects (+project), or contexts (@context)
- **📊 Statistics & Insights**: Get comprehensive stats about your productivity
- **🔄 todo.sh Integration**: Automatically works with existing [todo.sh](https://github.com/todotxt/todo.txt-cli) setups
- **💾 File Safety**: Automatic backups and configurable safety limits
- **⚡ Modern Installation**: Install with `uvx`, `uv`, `pipx`, or `pip`

## 🚀 Quick Start

### 1. Install

```bash
# Quick test (no installation required)
uvx todo-txt-mcp

# Install globally (recommended)
uv tool install todo-txt-mcp
```

<details>
<summary>More installation options</summary>

```bash
# Using pipx (isolated environment)
pipx install todo-txt-mcp

# Using pip (traditional)
pip install todo-txt-mcp
```

</details>

### 2. Configure Claude Desktop

Add to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "todo-txt": {
      "command": "uvx",
      "args": ["todo-txt-mcp"]
    }
  }
}
```

### 3. Restart Claude Desktop

Look for the 🔨 tools icon to confirm the server is connected.

## 💬 Example Conversations

Once configured, you can interact with your todos naturally:

> **You**: "Add a todo to call mom tomorrow with high priority"

> **You**: "Show me all my work-related todos"

> **You**: "What's my most important task right now?"

> **You**: "Mark the grocery shopping task as completed"

> **You**: "How many todos do I have in my @phone context?"

## 🛠️ Available Tools

The server provides these MCP tools for AI interaction:

| Tool | Description |
|------|-------------|
| `list_todos` | List all todos (with optional filters) |
| `add_todo` | Create new todo items |
| `complete_todo` | Mark todos as completed |
| `update_todo` | Modify existing todos |
| `delete_todo` | Remove todos |
| `search_todos` | Find todos by text content |
| `filter_by_priority` | Filter by priority level (A-Z) |
| `filter_by_project` | Filter by project tags (+project) |
| `filter_by_context` | Filter by context tags (@context) |
| `get_statistics` | Get comprehensive todo statistics |

## 📄 Todo.txt Format Support

Fully compatible with the [todo.txt specification](http://todotxt.org/):

```
(A) Call Mom +family @phone
x 2025-05-31 2025-05-30 (B) Buy groceries +shopping @errands
Write project proposal +work @computer
(C) Schedule dentist appointment +health @phone
```

## ⚙️ Configuration

### Works with Existing todo.sh Setup

If you're already using [todo.sh](https://github.com/todotxt/todo.txt-cli), the server automatically detects your configuration:

- `~/.todo/config`
- `~/.todo.cfg`
- `/etc/todo/config`
- `/usr/local/etc/todo/config`

### Custom Configuration

Specify a custom todo.txt file:

```json
{
  "mcpServers": {
    "todo-txt": {
      "command": "uvx",
      "args": ["todo-txt-mcp", "/path/to/your/todo.txt"]
    }
  }
}
```

### Environment Variables

Configure via environment variables:

```bash
TODO_MCP_TODO_FILE_PATH=/path/to/todo.txt
TODO_MCP_BACKUP_ENABLED=true
TODO_MCP_MAX_FILE_SIZE=10000000
```

## 🔒 Security & Privacy

- **Local only**: All processing happens on your machine
- **No network requests**: Your todos never leave your device
- **File safety**: Automatic backups and size limits
- **Sandboxed**: Only accesses configured todo.txt files

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- **Bug reports**: Use the [issue template](.github/ISSUE_TEMPLATE/bug_report.md)
- **Feature requests**: Use the [feature template](.github/ISSUE_TEMPLATE/feature_request.md)
- **Questions**: Start a [GitHub Discussion](https://github.com/danielmeint/todo-txt-mcp/discussions)

## 📋 Roadmap

- [ ] Due date support and reminders
- [ ] Recurring todos
- [ ] Multiple file support
- [ ] Sync capabilities
- [ ] Advanced search with regex
- [ ] Bulk operations

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Follows the [todo.txt format specification](http://todotxt.org/)
- Inspired by the [todo.sh](https://github.com/todotxt/todo.txt-cli) command-line tool
- Powered by [pytodotxt](https://github.com/regebro/pytodotxt) for parsing
