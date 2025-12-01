"""
Screen capture and interaction tools.

Provides X11-based screenshot capture and screen utilities.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


@dataclass
class ScreenInfo:
    """Information about screen/display."""

    width: int
    height: int
    display: str


class ScreenTools:
    """
    Screen capture and interaction utilities.

    Uses X11 tools for screenshot capture and screen information.
    """

    def __init__(self, display: Optional[str] = None) -> None:
        """
        Initialize screen tools.

        Args:
            display: X11 display (e.g., ":0"). Auto-detects if None.
        """
        self.display = display or os.environ.get("DISPLAY", ":0")

    def get_screen_info(self) -> Dict[str, Any]:
        """
        Get screen/display information.

        Returns:
            Dict with screen dimensions and display info, or error
        """
        try:
            # Use xdpyinfo to get screen info
            result = subprocess.run(
                ["xdpyinfo", "-display", self.display],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode != 0:
                return {"error": f"Failed to get screen info: {result.stderr}"}

            # Parse dimensions from output
            for line in result.stdout.split("\n"):
                if "dimensions:" in line:
                    # Format: "  dimensions:    1920x1080 pixels (508x285 millimeters)"
                    dims = line.split()[1].split("x")
                    width = int(dims[0])
                    height = int(dims[1].split()[0])

                    return {
                        "width": width,
                        "height": height,
                        "display": self.display,
                    }

            return {"error": "Could not parse screen dimensions"}

        except FileNotFoundError:
            return {"error": "xdpyinfo not found. Install: sudo apt install x11-utils"}
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": f"Error getting screen info: {e}"}

    def capture_screenshot(
        self, output_path: str, region: Optional[Tuple[int, int, int, int]] = None
    ) -> Dict[str, Any]:
        """
        Capture screenshot.

        Args:
            output_path: Path to save screenshot
            region: Optional (x, y, width, height) for region capture

        Returns:
            Dict with 'success' and 'path', or 'error'
        """
        try:
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Build command
            if region:
                x, y, w, h = region
                cmd = [
                    "import",
                    "-window",
                    "root",
                    "-crop",
                    f"{w}x{h}+{x}+{y}",
                    str(output_file),
                ]
            else:
                cmd = ["import", "-window", "root", str(output_file)]

            # Capture screenshot using ImageMagick's import
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                env={**os.environ, "DISPLAY": self.display},
            )

            if result.returncode != 0:
                return {"error": f"Screenshot failed: {result.stderr}"}

            if not output_file.exists():
                return {"error": "Screenshot file was not created"}

            return {"success": True, "path": str(output_file)}

        except FileNotFoundError:
            return {
                "error": "ImageMagick 'import' command not found. "
                "Install: sudo apt install imagemagick"
            }
        except subprocess.TimeoutExpired:
            return {"error": "Screenshot command timed out"}
        except Exception as e:
            return {"error": f"Error capturing screenshot: {e}"}

    def capture_screenshot_pil(
        self, output_path: str, region: Optional[Tuple[int, int, int, int]] = None
    ) -> Dict[str, Any]:
        """
        Capture screenshot using PIL/Pillow (alternative method).

        Args:
            output_path: Path to save screenshot
            region: Optional (x, y, width, height) for region capture

        Returns:
            Dict with 'success' and 'path', or 'error'
        """
        try:
            from PIL import ImageGrab
        except ImportError:
            return {
                "error": "Pillow not installed. Install: pip install Pillow"
            }

        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Capture
            if region:
                bbox = (region[0], region[1], region[0] + region[2], region[1] + region[3])
                screenshot = ImageGrab.grab(bbox=bbox)
            else:
                screenshot = ImageGrab.grab()

            # Save
            screenshot.save(output_file)

            return {"success": True, "path": str(output_file)}

        except Exception as e:
            return {"error": f"Error capturing screenshot with PIL: {e}"}

    def get_active_window_id(self) -> Dict[str, Any]:
        """
        Get the ID of the currently active window.

        Returns:
            Dict with 'window_id', or 'error'
        """
        try:
            result = subprocess.run(
                ["xdotool", "getactivewindow"],
                capture_output=True,
                text=True,
                timeout=5,
                env={**os.environ, "DISPLAY": self.display},
            )

            if result.returncode != 0:
                return {"error": f"Failed to get active window: {result.stderr}"}

            window_id = result.stdout.strip()
            return {"window_id": window_id}

        except FileNotFoundError:
            return {"error": "xdotool not found. Install: sudo apt install xdotool"}
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": f"Error getting active window: {e}"}
