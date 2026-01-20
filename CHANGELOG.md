# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-01-20

### Fixed
- **Input Sanitization**: Strip newlines from text inputs in `add_todo` and `update_todo` to prevent corrupting the todo.txt file structure (one line = one task)

### Changed
- **Repository Cleanup**: Simplified `.gitignore`, removed `.idea/` directory and unused `main.py`
- **Documentation**: Streamlined README for clarity, removed redundant sections
- **Development**: Added pre-commit hooks for ruff, black, mypy, and pytest

## [1.0.1] - 2025-05-31

### Fixed
- **Configuration Issue**: Fixed pydantic-settings configuration to ignore extra environment variables, preventing conflicts with unrelated environment variables like `PYPI_API_KEY`
- **Package Installation**: Resolved validation errors during package startup when extra environment variables are present

## [1.0.0] - 2025-05-31

### Added

#### Core Features
- **Full CRUD Operations**: Complete create, read, update, delete functionality for todo items
- **Todo.txt Format Compliance**: Full support for the [todo.txt specification](http://todotxt.org/)
- **Priority Support**: Handle priority levels (A-Z) with proper formatting
- **Projects & Contexts**: Complete support for +project and @context tags
- **File Safety**: Automatic backups and configurable file size limits
- **Search & Filtering**: Comprehensive search and filtering capabilities

#### MCP Tools
- `list_todos` - List all todos with optional completed items inclusion
- `get_todo` - Retrieve a specific todo by ID
- `search_todos` - Search todos by text content
- `filter_by_priority` - Filter todos by priority level (A-Z)
- `filter_by_project` - Filter todos by project tags
- `filter_by_context` - Filter todos by context tags
- `get_statistics` - Get comprehensive todo statistics
- `add_todo` - Add new todo items with full metadata support
- `complete_todo` - Mark todos as completed with timestamps
- `update_todo` - Update existing todo items
- `delete_todo` - Delete todo items
- `reload_todos` - Reload todos from file system

#### MCP Resources
- `todo://file` - Raw content access to todo.txt file
- `todo://stats` - Formatted statistics about your todos

#### Configuration & Integration
- **Todo.sh Integration**: Automatic detection and use of existing todo.sh configurations
- **Environment Variable Support**: Comprehensive configuration via environment variables
- **Multiple Installation Methods**: Support for uv, pip, pipx, and uvx
- **Cross-platform Support**: Works on macOS, Linux, and Windows

#### File Format Support
- **Todo Items**: Basic todo entries with proper parsing
- **Completion Markers**: Support for `x` completion indicators
- **Priority Levels**: Full (A) through (Z) priority support
- **Dates**: Creation and completion date handling
- **Projects**: +project tag support with filtering
- **Contexts**: @context tag support with filtering
- **Line Integrity**: Maintains proper todo.txt formatting

#### Safety & Reliability
- **Automatic Backups**: Configurable backup system with rotation
- **File Size Limits**: Prevent processing of oversized files
- **Error Handling**: Comprehensive error handling and validation
- **Input Sanitization**: Safe handling of user input

#### Development Features
- **Clean Architecture**: Separated models, services, and tools
- **Type Safety**: Full TypeScript-style type hints and validation
- **Test Coverage**: Comprehensive test suite with >90% coverage
- **Code Quality**: Black, Ruff, and MyPy integration

### Technical Details
- **Python Version**: Requires Python 3.10+
- **Dependencies**:
  - mcp[cli] >= 1.9.2
  - pydantic >= 2.11.5
  - pydantic-settings >= 2.9.0
  - pytodotxt >= 3.0.0
- **License**: MIT License
- **Package Format**: Modern Python packaging with pyproject.toml

### Documentation
- Comprehensive README with installation and usage examples
- API documentation for all MCP tools and resources
- Configuration guide with todo.sh integration examples
- Claude Desktop setup instructions
- Troubleshooting guide

### Distribution
- **PyPI Package**: Available as `todo-txt-mcp`
- **GitHub Repository**: Public repository with full source code
- **Entry Point**: Command-line script `todo-txt-mcp`
- **Build System**: Hatchling-based build system
- **Development Tools**: Complete development environment setup

## [Unreleased]

### Planned Features
- Due date support
- Recurring todos
- Advanced search with regex
- Bulk operations
- Import/export functionality
- Multiple file support
- Sync capabilities
- Web interface
- Plugin system

---

## Version History

- **v1.0.2** (2026-01-20): Bug fix for newline handling, repository cleanup, pre-commit hooks
- **v1.0.1** (2025-05-31): Fixed pydantic-settings configuration issue
- **v1.0.0** (2025-05-31): Initial stable release with full todo.txt MCP functionality
