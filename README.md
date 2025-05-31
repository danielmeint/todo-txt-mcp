# Todo.txt MCP Server

A minimal but extensible Model Context Protocol (MCP) server that exposes todo.txt files through a structured API for use with AI clients like Claude Desktop.

## Features

### Phase 1 MVP (Current)

- ✅ **Full CRUD Operations**: Create, read, update, delete todos
- ✅ **Todo.txt Format Compliance**: Follows the [todo.txt specification](http://todotxt.org/)
- ✅ **Priority Support**: Handle priority levels (A-Z)
- ✅ **Projects & Contexts**: Support for +project and @context tags
- ✅ **Search & Filtering**: Search by text, filter by priority, project, or context
- ✅ **Statistics**: Get comprehensive stats about your todo list
- ✅ **File Safety**: Automatic backups and file size limits
- ✅ **MCP Resources**: Access raw file content and formatted statistics

### Available MCP Tools

#### List & Query Tools
- `list_todos` - List all todos (optionally include completed)
- `get_todo` - Get a specific todo by ID
- `search_todos` - Search todos by text content
- `filter_by_priority` - Filter todos by priority level
- `filter_by_project` - Filter todos by project
- `filter_by_context` - Filter todos by context
- `get_statistics` - Get comprehensive todo statistics

#### CRUD Tools
- `add_todo` - Add a new todo item
- `complete_todo` - Mark a todo as completed
- `update_todo` - Update an existing todo
- `delete_todo` - Delete a todo item
- `reload_todos` - Reload todos from file system

### Available MCP Resources
- `todo://file` - Raw content of the todo.txt file
- `todo://stats` - Formatted statistics about your todos

## Installation

### Quick Start (Recommended)

The fastest way to get started is using `uvx` to run the server without installing:

```bash
# Run directly without installing (recommended for testing)
uvx todo-txt-mcp

# Or install globally with uv
uv tool install todo-txt-mcp
```

### Installation Methods

#### 1. Using uv (Modern Python Package Manager)

```bash
# Install globally (recommended)
uv tool install todo-txt-mcp

# Or install in project
uv add todo-txt-mcp

# Run the server
uv tool run todo-txt-mcp
# or if installed in project: uv run todo-txt-mcp
```

#### 2. Using pip (Traditional)

```bash
# Install globally
pip install todo-txt-mcp

# Or install for user only
pip install --user todo-txt-mcp

# Run the server
todo-txt-mcp
```

#### 3. Using pipx (Isolated Installation)

```bash
# Install in isolated environment
pipx install todo-txt-mcp

# Run the server
todo-txt-mcp
```

### From Source

```bash
git clone https://github.com/danielmeint/todo-txt-mcp.git
cd todo-txt-mcp
uv install
```

### Development Installation

```bash
git clone https://github.com/danielmeint/todo-txt-mcp.git
cd todo-txt-mcp
uv install --dev
```

## Usage

### Command Line

Run the MCP server directly:

```bash
# Use default todo.txt in current directory
todo-txt-mcp

# Specify a custom todo.txt file
todo-txt-mcp /path/to/your/todo.txt

# Use existing todo.sh configuration (auto-detected)
todo-txt-mcp

# Specify a todo.sh config file explicitly  
todo-txt-mcp /path/to/your/todo.cfg
```

### Integration with Existing todo.sh Setup

If you're already using [todo.sh](https://github.com/todotxt/todo.txt-cli), this MCP server can automatically use your existing configuration! 

The server will automatically detect and use todo.sh config files in these locations:
- `~/.todo/config`
- `~/.todo.cfg` 
- `/etc/todo/config`
- `/usr/local/etc/todo/config`

Your existing todo.sh config variables are supported:
- `TODO_DIR` - Base directory for todo files
- `TODO_FILE` - Path to your todo.txt file
- `DONE_FILE` - Path to your done.txt file

Example todo.sh config:
```bash
# Your todo.txt directory
export TODO_DIR="/Users/username/Dropbox/todo"

# Your todo/done/report.txt locations  
export TODO_FILE="$TODO_DIR/todo.txt"
export DONE_FILE="$TODO_DIR/done.txt"
export REPORT_FILE="$TODO_DIR/report.txt"
```

### With Claude Desktop

Add to your Claude Desktop MCP configuration file:

**Location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Option 1: Using uvx (Recommended)
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

#### Option 2: Using uv tool
```json
{
  "mcpServers": {
    "todo-txt": {
      "command": "uv",
      "args": ["tool", "run", "todo-txt-mcp"]
    }
  }
}
```

#### Option 3: Direct installation
```json
{
  "mcpServers": {
    "todo-txt": {
      "command": "todo-txt-mcp"
    }
  }
}
```

#### Option 4: With custom todo.txt file
```json
{
  "mcpServers": {
    "todo-txt": {
      "command": "uvx",
      "args": ["todo-txt-mcp", "/Users/username/Dropbox/todo/todo.txt"]
    }
  }
}
```

#### Option 5: With environment variables
```json
{
  "mcpServers": {
    "todo-txt": {
      "command": "uvx",
      "args": ["todo-txt-mcp"],
      "env": {
        "TODO_MCP_TODO_FILE_PATH": "/Users/username/Dropbox/todo/todo.txt",
        "TODO_MCP_BACKUP_ENABLED": "true"
      }
    }
  }
}
```

**Restart Claude Desktop** after updating the configuration file.

### Configuration

#### Using Existing todo.sh Configuration (Recommended)

If you already use [todo.sh](https://github.com/todotxt/todo.txt-cli), no additional configuration is needed! The MCP server will automatically detect and use your existing todo.sh config.

#### Manual Configuration 

The server can also be configured via environment variables:

```bash
# File paths
TODO_MCP_TODO_FILE_PATH=/path/to/todo.txt
TODO_MCP_DONE_FILE_PATH=/path/to/done.txt

# File handling
TODO_MCP_ENCODING=utf-8
TODO_MCP_AUTO_ARCHIVE=true
TODO_MCP_BACKUP_ENABLED=true
TODO_MCP_BACKUP_COUNT=5

# Safety limits
TODO_MCP_MAX_FILE_SIZE=10000000  # 10MB
```

## Examples

### Adding Todos

```python
# Add a simple todo
add_todo(text="Buy groceries")

# Add a todo with priority and tags
add_todo(
    text="Finish project proposal", 
    priority="A",
    projects=["work"],
    contexts=["computer", "office"]
)
```

### Searching and Filtering

```python
# Search for todos containing "meeting"
search_todos(query="meeting")

# Get all high-priority todos
filter_by_priority(priority="A")

# Get all work-related todos
filter_by_project(project="work")

# Get all todos for phone calls
filter_by_context(context="phone")
```

### Managing Todos

```python
# Complete a todo
complete_todo(todo_id="abc123")

# Update a todo
update_todo(
    todo_id="abc123",
    text="Updated task description",
    priority="B"
)

# Delete a todo
delete_todo(todo_id="abc123")
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/test_todo_service.py
```

### Project Structure

```
src/todo_txt_mcp/
├── __init__.py          # Package initialization
├── server.py            # Main MCP server
├── models/              # Data models
│   ├── config.py        # Configuration model
│   └── todo.py          # Todo item and list models
├── services/            # Business logic
│   ├── file_service.py  # File I/O operations
│   └── todo_service.py  # Todo business logic
└── tools/               # MCP tools
    ├── crud_tools.py    # Create/Update/Delete tools
    └── list_tools.py    # List/Query tools
```

### Architecture

The server follows a clean architecture pattern:

1. **Models**: Pydantic models for data validation and serialization
2. **Services**: Business logic layer that handles todo operations
3. **Tools**: MCP tool definitions that expose functionality to clients
4. **Server**: FastMCP server that ties everything together

## Todo.txt Format Support

The server fully supports the [todo.txt format specification](http://todotxt.org/):

- ✅ Basic todo items
- ✅ Completion markers (`x`)
- ✅ Priority levels (`(A)` through `(Z)`)
- ✅ Creation and completion dates
- ✅ Projects (`+project`)
- ✅ Contexts (`@context`)
- ✅ Proper formatting and parsing

Example todo.txt content:
```
(A) Call Mom +family @phone
x 2024-01-15 2024-01-10 (B) Buy groceries +shopping @errands
Write project proposal +work @computer
(C) Schedule dentist appointment +health @phone
```

## Roadmap

### Phase 2 (Planned)
- [ ] Due date support
- [ ] Recurring todos
- [ ] Advanced search with regex
- [ ] Bulk operations
- [ ] Import/export functionality

### Phase 3 (Planned)
- [ ] Multiple file support
- [ ] Sync capabilities
- [ ] Web interface
- [ ] Plugin system
- [ ] Advanced reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

[Add your license here]

## Acknowledgments

- Built with [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol)
- Uses [pytodotxt](https://github.com/regebro/pytodotxt) for todo.txt parsing
- Follows the [todo.txt format](http://todotxt.org/) specification
