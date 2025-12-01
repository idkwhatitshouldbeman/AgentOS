"""
Vision model interface for screen understanding.

Provides abstract interface for vision models (future integration).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional


class VisionBackend(ABC):
    """Abstract interface for vision models."""

    @abstractmethod
    def analyze_image(self, image_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze an image and return structured understanding.

        Args:
            image_path: Path to image file
            prompt: Optional prompt/question about the image

        Returns:
            Dict with analysis results or error
        """
        raise NotImplementedError


class StubVisionBackend(VisionBackend):
    """
    Stub vision backend for testing.

    Returns placeholder responses.
    """

    def analyze_image(self, image_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """Return stub response."""
        image_file = Path(image_path)
        
        if not image_file.exists():
            return {"error": f"Image not found: {image_path}"}

        return {
            "description": f"[STUB] Image analysis for {image_file.name}",
            "objects": [],
            "text": "",
            "note": "Vision backend not yet implemented. Future: LLaVA, moondream, or similar.",
        }


# TODO: Future vision model integrations
# 
# class LLaVABackend(VisionBackend):
#     """LLaVA vision model backend."""
#     pass
#
# class MoondreamBackend(VisionBackend):
#     """Moondream vision model backend."""
#     pass


def get_vision_backend(backend_type: str = "stub") -> VisionBackend:
    """
    Get vision backend instance.

    Args:
        backend_type: Backend type ("stub", "llava", "moondream", etc.)

    Returns:
        VisionBackend instance
    """
    if backend_type == "stub":
        return StubVisionBackend()
    else:
        raise ValueError(f"Unknown vision backend: {backend_type}")
