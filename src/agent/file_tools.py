"""
File management tools implementation.

These tools allow the AI to read, write, and manage files with proper safety checks.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List


class FileTools:
    """
    File operation tools with safety checks.

    All operations are restricted to user's home directory by default,
    with explicit allowlists for system paths if needed.
    """

    def __init__(self, allowed_paths: List[str] | None = None, home_dir: str | None = None) -> None:
        """
        Initialize file tools.

        Args:
            allowed_paths: List of allowed absolute paths (defaults to home directory)
            home_dir: Home directory path (defaults to $HOME)
        """
        self.home_dir = Path(home_dir or os.path.expanduser("~"))
        self.allowed_paths = [Path(p) for p in (allowed_paths or [str(self.home_dir)])]

    def _check_path_allowed(self, path: Path) -> bool:
        """Check if a path is within allowed directories."""
        path = path.resolve()
        return any(path.is_relative_to(allowed) for allowed in self.allowed_paths)

    def _ensure_path_allowed(self, path: Path) -> None:
        """Raise ValueError if path is not allowed."""
        if not self._check_path_allowed(path):
            raise ValueError(f"Path {path} is not in allowed directories")

    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read file contents.

        Returns:
            Dict with 'content' (str) or 'error' (str)
        """
        try:
            file_path = Path(path)
            if not file_path.is_absolute():
                file_path = self.home_dir / file_path

            self._ensure_path_allowed(file_path)

            if not file_path.exists():
                return {"error": f"File not found: {file_path}"}

            if not file_path.is_file():
                return {"error": f"Path is not a file: {file_path}"}

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            return {"content": content, "path": str(file_path)}

        except ValueError as e:
            return {"error": str(e)}
        except PermissionError:
            return {"error": f"Permission denied: {file_path}"}
        except Exception as e:
            return {"error": f"Error reading file: {e}"}

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write content to file.

        Returns:
            Dict with 'success' (bool) and 'path' (str) or 'error' (str)
        """
        try:
            file_path = Path(path)
            if not file_path.is_absolute():
                file_path = self.home_dir / file_path

            self._ensure_path_allowed(file_path)

            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {"success": True, "path": str(file_path)}

        except ValueError as e:
            return {"error": str(e)}
        except PermissionError:
            return {"error": f"Permission denied: {file_path}"}
        except Exception as e:
            return {"error": f"Error writing file: {e}"}

    def list_directory(self, path: str) -> Dict[str, Any]:
        """
        List directory contents.

        Returns:
            Dict with 'entries' (list of dicts) or 'error' (str)
        """
        try:
            dir_path = Path(path)
            if not dir_path.is_absolute():
                dir_path = self.home_dir / dir_path

            self._ensure_path_allowed(dir_path)

            if not dir_path.exists():
                return {"error": f"Directory not found: {dir_path}"}

            if not dir_path.is_dir():
                return {"error": f"Path is not a directory: {dir_path}"}

            entries = []
            for item in sorted(dir_path.iterdir()):
                entries.append(
                    {
                        "name": item.name,
                        "path": str(item),
                        "type": "directory" if item.is_dir() else "file",
                        "size": item.stat().st_size if item.is_file() else None,
                    }
                )

            return {"entries": entries, "path": str(dir_path)}

        except ValueError as e:
            return {"error": str(e)}
        except PermissionError:
            return {"error": f"Permission denied: {dir_path}"}
        except Exception as e:
            return {"error": f"Error listing directory: {e}"}

    def move_file(self, src: str, dst: str) -> Dict[str, Any]:
        """
        Move or rename a file.

        Returns:
            Dict with 'success' (bool) or 'error' (str)
        """
        try:
            src_path = Path(src)
            dst_path = Path(dst)

            if not src_path.is_absolute():
                src_path = self.home_dir / src_path
            if not dst_path.is_absolute():
                dst_path = self.home_dir / dst_path

            self._ensure_path_allowed(src_path)
            self._ensure_path_allowed(dst_path)

            if not src_path.exists():
                return {"error": f"Source file not found: {src_path}"}

            shutil.move(str(src_path), str(dst_path))

            return {"success": True, "src": str(src_path), "dst": str(dst_path)}

        except ValueError as e:
            return {"error": str(e)}
        except PermissionError:
            return {"error": f"Permission denied"}
        except Exception as e:
            return {"error": f"Error moving file: {e}"}

    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete a file or directory.

        Returns:
            Dict with 'success' (bool) or 'error' (str)
        """
        try:
            file_path = Path(path)
            if not file_path.is_absolute():
                file_path = self.home_dir / file_path

            self._ensure_path_allowed(file_path)

            if not file_path.exists():
                return {"error": f"Path not found: {file_path}"}

            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()

            return {"success": True, "path": str(file_path)}

        except ValueError as e:
            return {"error": str(e)}
        except PermissionError:
            return {"error": f"Permission denied: {file_path}"}
        except Exception as e:
            return {"error": f"Error deleting: {e}"}

