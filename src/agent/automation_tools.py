"""
UI automation tools for mouse and keyboard control.

Provides xdotool-based automation for clicking, typing, and key combinations.
"""

from __future__ import annotations

import os
import subprocess
import time
from typing import Any, Dict, List, Optional


class AutomationTools:
    """
    UI automation using xdotool for mouse and keyboard control.
    """

    def __init__(self, display: Optional[str] = None) -> None:
        """
        Initialize automation tools.

        Args:
            display: X11 display (e.g., ":0"). Auto-detects if None.
        """
        self.display = display or os.environ.get("DISPLAY", ":0")

    def _run_xdotool(self, args: List[str]) -> Dict[str, Any]:
        """
        Run xdotool command.

        Args:
            args: Command arguments

        Returns:
            Dict with 'success' and optionally 'output', or 'error'
        """
        try:
            result = subprocess.run(
                ["xdotool"] + args,
                capture_output=True,
                text=True,
                timeout=10,
                env={**os.environ, "DISPLAY": self.display},
            )

            if result.returncode != 0:
                return {"error": f"xdotool failed: {result.stderr}"}

            return {"success": True, "output": result.stdout.strip()}

        except FileNotFoundError:
            return {"error": "xdotool not found. Install: sudo apt install xdotool"}
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": f"Error running xdotool: {e}"}

    def click(self, x: int, y: int, button: int = 1) -> Dict[str, Any]:
        """
        Click at screen coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            button: Mouse button (1=left, 2=middle, 3=right)

        Returns:
            Dict with 'success' or 'error'
        """
        result = self._run_xdotool(["mousemove", str(x), str(y)])
        if "error" in result:
            return result

        return self._run_xdotool(["click", str(button)])

    def double_click(self, x: int, y: int) -> Dict[str, Any]:
        """
        Double-click at screen coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Dict with 'success' or 'error'
        """
        result = self._run_xdotool(["mousemove", str(x), str(y)])
        if "error" in result:
            return result

        return self._run_xdotool(["click", "--repeat", "2", "1"])

    def move_mouse(self, x: int, y: int) -> Dict[str, Any]:
        """
        Move mouse to coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Dict with 'success' or 'error'
        """
        return self._run_xdotool(["mousemove", str(x), str(y)])

    def type_text(self, text: str, delay: int = 12) -> Dict[str, Any]:
        """
        Type text at current focus.

        Args:
            text: Text to type
            delay: Delay between keystrokes in milliseconds

        Returns:
            Dict with 'success' or 'error'
        """
        return self._run_xdotool(["type", "--delay", str(delay), text])

    def press_key(self, key: str) -> Dict[str, Any]:
        """
        Press a key or key combination.

        Args:
            key: Key name (e.g., "Return", "ctrl+c", "alt+Tab")

        Returns:
            Dict with 'success' or 'error'
        """
        return self._run_xdotool(["key", key])

    def press_keys(self, keys: List[str], delay: int = 100) -> Dict[str, Any]:
        """
        Press multiple keys in sequence.

        Args:
            keys: List of key names
            delay: Delay between key presses in milliseconds

        Returns:
            Dict with 'success' or 'error'
        """
        for key in keys:
            result = self.press_key(key)
            if "error" in result:
                return result
            if delay > 0:
                time.sleep(delay / 1000.0)

        return {"success": True}

    def get_mouse_location(self) -> Dict[str, Any]:
        """
        Get current mouse cursor location.

        Returns:
            Dict with 'x', 'y' coordinates, or 'error'
        """
        result = self._run_xdotool(["getmouselocation", "--shell"])
        if "error" in result:
            return result

        # Parse output (format: "X=123\nY=456\nSCREEN=0\nWINDOW=12345")
        try:
            lines = result["output"].split("\n")
            x = int(lines[0].split("=")[1])
            y = int(lines[1].split("=")[1])
            return {"x": x, "y": y}
        except (IndexError, ValueError) as e:
            return {"error": f"Failed to parse mouse location: {e}"}

    def focus_window(self, window_id: str) -> Dict[str, Any]:
        """
        Focus a specific window.

        Args:
            window_id: X11 window ID

        Returns:
            Dict with 'success' or 'error'
        """
        return self._run_xdotool(["windowfocus", window_id])

    def search_window(self, name_pattern: str) -> Dict[str, Any]:
        """
        Search for windows by name.

        Args:
            name_pattern: Window name pattern (regex)

        Returns:
            Dict with 'window_ids' list, or 'error'
        """
        result = self._run_xdotool(["search", "--name", name_pattern])
        if "error" in result:
            return result

        window_ids = result["output"].split("\n") if result["output"] else []
        return {"window_ids": [wid for wid in window_ids if wid]}
