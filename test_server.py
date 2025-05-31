#!/usr/bin/env python3
"""Simple test script to verify the MCP server works."""

import asyncio
import tempfile
from pathlib import Path

from src.todo_txt_mcp.models.config import TodoMCPConfig
from src.todo_txt_mcp.server import create_server


async def test_server_creation():
    """Test that we can create the MCP server."""
    print("Testing MCP server creation...")

    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create config with temporary file
        config = TodoMCPConfig(
            todo_file_path=temp_path / "todo.txt", backup_enabled=False
        )

        # Create the server
        server = create_server(config=config)

        print(f"✅ Server created successfully: {server.name}")
        print(f"✅ Todo file path: {config.todo_file_path}")

        # Test that we can access the tools
        tools = await server.list_tools()
        print(f"✅ Available tools: {len(tools)} tools")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")

        # Test that we can access resources
        resources = await server.list_resources()
        print(f"✅ Available resources: {len(resources)} resources")
        for resource in resources:
            print(f"   - {resource.uri}: {resource.description}")

        print(
            "\n🎉 Phase 1 MVP is working! The server can be created and exposes tools and resources."
        )
        return True


if __name__ == "__main__":
    asyncio.run(test_server_creation())
