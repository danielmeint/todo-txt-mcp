"""Unit tests for TodoService."""

from src.todo_txt_mcp.services.todo_service import TodoService


def test_add_todo(todo_service: TodoService):
    """Test adding a new todo."""
    todo = todo_service.add_todo("Test todo item")

    assert todo.text == "Test todo item"
    assert not todo.completed
    assert todo.id is not None
    assert todo.creation_date is not None


def test_add_todo_with_priority_and_tags(todo_service: TodoService):
    """Test adding a todo with priority, projects, and contexts."""
    todo = todo_service.add_todo(
        text="Important task",
        priority="A",
        projects={"work", "urgent"},
        contexts={"office", "computer"},
    )

    assert todo.text == "Important task"
    assert todo.priority == "A"
    assert todo.projects == {"work", "urgent"}
    assert todo.contexts == {"office", "computer"}


def test_list_todos_empty(todo_service: TodoService):
    """Test listing todos when none exist."""
    todos = todo_service.list_todos()
    assert len(todos) == 0


def test_list_todos_with_items(todo_service: TodoService):
    """Test listing todos after adding some."""
    todo_service.add_todo("First todo")
    todo_service.add_todo("Second todo")

    todos = todo_service.list_todos()
    assert len(todos) == 2
    assert todos[0].text == "First todo"
    assert todos[1].text == "Second todo"


def test_complete_todo(todo_service: TodoService):
    """Test completing a todo."""
    todo = todo_service.add_todo("Todo to complete")

    success = todo_service.complete_todo(todo.id)
    assert success

    # Verify the todo is marked as completed
    updated_todo = todo_service.get_todo(todo.id)
    assert updated_todo.completed
    assert updated_todo.completion_date is not None


def test_complete_nonexistent_todo(todo_service: TodoService):
    """Test completing a todo that doesn't exist."""
    success = todo_service.complete_todo("nonexistent-id")
    assert not success


def test_update_todo(todo_service: TodoService):
    """Test updating a todo."""
    todo = todo_service.add_todo("Original text")

    success = todo_service.update_todo(
        todo.id,
        text="Updated text",
        priority="B",
        projects={"project1"},
        contexts={"context1"},
    )
    assert success

    # Verify the updates
    updated_todo = todo_service.get_todo(todo.id)
    assert updated_todo.text == "Updated text"
    assert updated_todo.priority == "B"
    assert updated_todo.projects == {"project1"}
    assert updated_todo.contexts == {"context1"}


def test_delete_todo(todo_service: TodoService):
    """Test deleting a todo."""
    todo = todo_service.add_todo("Todo to delete")

    success = todo_service.delete_todo(todo.id)
    assert success

    # Verify the todo is gone
    deleted_todo = todo_service.get_todo(todo.id)
    assert deleted_todo is None


def test_search_todos(todo_service: TodoService):
    """Test searching todos by text."""
    todo_service.add_todo("Buy groceries")
    todo_service.add_todo("Call mom")
    todo_service.add_todo("Buy birthday gift")

    # Search for "buy"
    results = todo_service.search_todos("buy")
    assert len(results) == 2
    assert all("buy" in todo.text.lower() for todo in results)


def test_filter_by_priority(todo_service: TodoService):
    """Test filtering todos by priority."""
    todo_service.add_todo("High priority task", priority="A")
    todo_service.add_todo("Medium priority task", priority="B")
    todo_service.add_todo("Low priority task", priority="C")
    todo_service.add_todo("No priority task")

    # Filter by priority A
    results = todo_service.filter_by_priority("A")
    assert len(results) == 1
    assert results[0].priority == "A"


def test_filter_by_project(todo_service: TodoService):
    """Test filtering todos by project."""
    todo_service.add_todo("Work task", projects={"work"})
    todo_service.add_todo("Home task", projects={"home"})
    todo_service.add_todo("Mixed task", projects={"work", "urgent"})

    # Filter by work project
    results = todo_service.filter_by_project("work")
    assert len(results) == 2
    assert all("work" in todo.projects for todo in results)


def test_filter_by_context(todo_service: TodoService):
    """Test filtering todos by context."""
    todo_service.add_todo("Phone call", contexts={"phone"})
    todo_service.add_todo("Computer work", contexts={"computer"})
    todo_service.add_todo("Office meeting", contexts={"office", "meeting"})

    # Filter by phone context
    results = todo_service.filter_by_context("phone")
    assert len(results) == 1
    assert "phone" in results[0].contexts


def test_get_statistics(todo_service: TodoService):
    """Test getting todo statistics."""
    # Add some todos with different properties
    todo_service.add_todo("High priority", priority="A")
    todo_service.add_todo("Medium priority", priority="B")
    todo_service.add_todo("Work task", projects={"work"}, contexts={"office"})

    # Complete one todo
    todos = todo_service.list_todos()
    todo_service.complete_todo(todos[0].id)

    stats = todo_service.get_statistics()

    assert stats["total_todos"] == 3
    assert stats["active_todos"] == 2
    assert stats["completed_todos"] == 1
    assert "A" in stats["priority_counts"] or "B" in stats["priority_counts"]
    assert "work" in stats["projects"]
    assert "office" in stats["contexts"]
