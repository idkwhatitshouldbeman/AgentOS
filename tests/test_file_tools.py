"""
Tests for file management tools.
"""

import os
import tempfile
from pathlib import Path

import pytest

from agent.file_tools import FileTools


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def file_tools(temp_dir):
    """Create FileTools instance with temp directory as allowed path."""
    return FileTools(allowed_paths=[temp_dir], home_dir=temp_dir)


def test_read_file_success(file_tools, temp_dir):
    """Test reading an existing file."""
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("Hello, world!")

    result = file_tools.read_file(str(test_file))

    assert "error" not in result
    assert result["content"] == "Hello, world!"
    assert result["path"] == str(test_file)


def test_read_file_not_found(file_tools, temp_dir):
    """Test reading a non-existent file."""
    result = file_tools.read_file(str(Path(temp_dir) / "nonexistent.txt"))

    assert "error" in result
    assert "not found" in result["error"].lower()


def test_read_file_path_not_allowed(file_tools):
    """Test that reading files outside allowed paths fails."""
    result = file_tools.read_file("/etc/passwd")

    assert "error" in result
    assert "not in allowed" in result["error"].lower()


def test_write_file_success(file_tools, temp_dir):
    """Test writing a file."""
    test_file = Path(temp_dir) / "new_file.txt"

    result = file_tools.write_file(str(test_file), "Test content")

    assert "error" not in result
    assert result["success"] is True
    assert test_file.exists()
    assert test_file.read_text() == "Test content"


def test_write_file_creates_parent_dirs(file_tools, temp_dir):
    """Test that write_file creates parent directories."""
    test_file = Path(temp_dir) / "subdir" / "nested" / "file.txt"

    result = file_tools.write_file(str(test_file), "Nested content")

    assert "error" not in result
    assert result["success"] is True
    assert test_file.exists()


def test_list_directory_success(file_tools, temp_dir):
    """Test listing directory contents."""
    # Create some test files
    (Path(temp_dir) / "file1.txt").write_text("content1")
    (Path(temp_dir) / "file2.txt").write_text("content2")
    (Path(temp_dir) / "subdir").mkdir()

    result = file_tools.list_directory(temp_dir)

    assert "error" not in result
    assert "entries" in result
    assert len(result["entries"]) == 3

    names = [e["name"] for e in result["entries"]]
    assert "file1.txt" in names
    assert "file2.txt" in names
    assert "subdir" in names


def test_move_file_success(file_tools, temp_dir):
    """Test moving a file."""
    src = Path(temp_dir) / "source.txt"
    dst = Path(temp_dir) / "dest.txt"
    src.write_text("Move me")

    result = file_tools.move_file(str(src), str(dst))

    assert "error" not in result
    assert result["success"] is True
    assert not src.exists()
    assert dst.exists()
    assert dst.read_text() == "Move me"


def test_delete_file_success(file_tools, temp_dir):
    """Test deleting a file."""
    test_file = Path(temp_dir) / "to_delete.txt"
    test_file.write_text("Delete me")

    result = file_tools.delete_file(str(test_file))

    assert "error" not in result
    assert result["success"] is True
    assert not test_file.exists()


def test_delete_directory_success(file_tools, temp_dir):
    """Test deleting a directory."""
    test_dir = Path(temp_dir) / "to_delete_dir"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("content")

    result = file_tools.delete_file(str(test_dir))

    assert "error" not in result
    assert result["success"] is True
    assert not test_dir.exists()


def test_relative_paths_use_home_dir(file_tools, temp_dir):
    """Test that relative paths are resolved relative to home_dir."""
    result = file_tools.write_file("relative.txt", "content")

    assert "error" not in result
    assert (Path(temp_dir) / "relative.txt").exists()


def test_safety_check_prevents_outside_access(file_tools):
    """Test that safety checks prevent accessing files outside allowed paths."""
    # Try to write to /tmp (should fail if not in allowed_paths)
    result = file_tools.write_file("/tmp/test.txt", "hack attempt")

    assert "error" in result
    assert "not in allowed" in result["error"].lower()

