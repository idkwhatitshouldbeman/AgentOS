"""
Enhanced screen capture and vision tools.
Provides screen capture, OCR, and visual understanding.
"""

from __future__ import annotations

import base64
import io
import os
import subprocess
import time
from typing import Any, Dict, List, Optional

try:
    from PIL import Image, ImageGrab
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False


class ScreenToolsEnhanced:
    """
    Enhanced screen capture and vision tools.
    """

    def __init__(self, display: Optional[str] = None):
        """
        Initialize screen tools.
        
        Args:
            display: X11 display (e.g., ":0"). Auto-detects if None.
        """
        self.display = display or os.environ.get("DISPLAY", ":0")
        self.last_capture: Optional[bytes] = None

    def capture_screen(self, format: str = "png") -> Dict[str, Any]:
        """
        Capture the entire screen.
        
        Args:
            format: Image format (png, jpeg)
            
        Returns:
            Dict with image data (base64) or error
        """
        try:
            if not HAS_PIL:
                # Fallback to xwd + convert
                return self._capture_via_xwd(format)
            
            # Use PIL for screen capture
            screenshot = ImageGrab.grab()
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format=format.upper())
            img_bytes.seek(0)
            self.last_capture = img_bytes.read()
            
            # Encode to base64
            img_base64 = base64.b64encode(self.last_capture).decode('utf-8')
            
            return {
                "success": True,
                "format": format,
                "width": screenshot.width,
                "height": screenshot.height,
                "data": img_base64,
                "size_bytes": len(self.last_capture),
            }
        except Exception as e:
            return {"error": f"Error capturing screen: {e}"}

    def _capture_via_xwd(self, format: str) -> Dict[str, Any]:
        """Fallback screen capture using xwd."""
        try:
            # Use xwd to capture screen
            xwd_process = subprocess.Popen(
                ["xwd", "-root", "-out", "/tmp/screenshot.xwd"],
                env={**os.environ, "DISPLAY": self.display},
            )
            xwd_process.wait()
            
            # Convert to PNG using ImageMagick or PIL
            if HAS_PIL:
                img = Image.open("/tmp/screenshot.xwd")
                img_bytes = io.BytesIO()
                img.save(img_bytes, format=format.upper())
                img_bytes.seek(0)
                self.last_capture = img_bytes.read()
                img_base64 = base64.b64encode(self.last_capture).decode('utf-8')
                
                return {
                    "success": True,
                    "format": format,
                    "width": img.width,
                    "height": img.height,
                    "data": img_base64,
                }
            else:
                # Use convert command
                subprocess.run(
                    ["convert", "/tmp/screenshot.xwd", f"/tmp/screenshot.{format}"],
                    check=True,
                )
                with open(f"/tmp/screenshot.{format}", "rb") as f:
                    self.last_capture = f.read()
                    img_base64 = base64.b64encode(self.last_capture).decode('utf-8')
                
                return {
                    "success": True,
                    "format": format,
                    "data": img_base64,
                }
        except Exception as e:
            return {"error": f"Error capturing via xwd: {e}"}

    def capture_region(self, x: int, y: int, width: int, height: int, format: str = "png") -> Dict[str, Any]:
        """
        Capture a specific region of the screen.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Region width
            height: Region height
            format: Image format
            
        Returns:
            Dict with image data or error
        """
        try:
            if not HAS_PIL:
                return {"error": "PIL required for region capture"}
            
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format=format.upper())
            img_bytes.seek(0)
            img_data = img_bytes.read()
            
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            
            return {
                "success": True,
                "format": format,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "data": img_base64,
            }
        except Exception as e:
            return {"error": f"Error capturing region: {e}"}

    def extract_text_from_screen(self, x: Optional[int] = None, y: Optional[int] = None, 
                                  width: Optional[int] = None, height: Optional[int] = None) -> Dict[str, Any]:
        """
        Extract text from screen using OCR.
        
        Args:
            x, y, width, height: Optional region to OCR (if None, uses full screen)
            
        Returns:
            Dict with extracted text or error
        """
        if not HAS_OCR:
            return {"error": "pytesseract not installed. Install: sudo apt install tesseract-ocr"}
        
        try:
            # Capture screen or region
            if x is not None and y is not None and width is not None and height is not None:
                capture_result = self.capture_region(x, y, width, height)
            else:
                capture_result = self.capture_screen()
            
            if "error" in capture_result:
                return capture_result
            
            # Decode image
            img_data = base64.b64decode(capture_result["data"])
            img = Image.open(io.BytesIO(img_data))
            
            # Extract text
            text = pytesseract.image_to_string(img)
            
            return {
                "success": True,
                "text": text.strip(),
                "confidence": "N/A",  # pytesseract can provide confidence with image_to_data
            }
        except Exception as e:
            return {"error": f"Error extracting text: {e}"}

    def get_screen_resolution(self) -> Dict[str, Any]:
        """
        Get screen resolution.
        
        Returns:
            Dict with screen resolution
        """
        try:
            if HAS_PIL:
                screenshot = ImageGrab.grab()
                return {
                    "success": True,
                    "width": screenshot.width,
                    "height": screenshot.height,
                }
            else:
                # Use xrandr
                result = subprocess.run(
                    ["xrandr"],
                    capture_output=True,
                    text=True,
                    env={**os.environ, "DISPLAY": self.display},
                )
                
                # Parse output
                for line in result.stdout.split('\n'):
                    if '*' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if '*' in part:
                                resolution = parts[i-1]
                                width, height = map(int, resolution.split('x'))
                                return {
                                    "success": True,
                                    "width": width,
                                    "height": height,
                                }
                
                return {"error": "Could not determine screen resolution"}
        except Exception as e:
            return {"error": f"Error getting resolution: {e}"}

