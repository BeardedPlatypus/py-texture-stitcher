from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


SUFFIX = ".png.stitch.json"


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> Version:
        return cls(**input_dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
        }

    def to_str(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class Dimension:
    x: int
    y: int

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> Dimension:
        return cls(**input_dict)

    def to_dict(self) -> Dict[str, int]:
        return {
            "x": self.x,
            "y": self.y,
        }

    def to_str(self) -> str:
        return f"{self.x}, {self.y}"


class StitchDescriptionMetadata:
    @property
    def version(self) -> Version:
        return Version(1, 0, 0)

    def to_dict(self) -> Dict[str, Any]:
        return {"stitch_description": True, "version": self.version.to_dict()}


@dataclass
class StitchDescription:
    @property
    def metadata(self) -> StitchDescriptionMetadata:
        return StitchDescriptionMetadata()

    image_paths: Sequence[Path]
    stitch_dimension: Dimension
    image_dimension: Dimension

    @staticmethod
    def _is_stitch_description(input_dict: Dict[str, Any]) -> bool:
        return input_dict.get("metadata", {}).get("stitch_description", False)

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> Optional[StitchDescription]:
        if not cls._is_stitch_description(input_dict):
            return None

        return cls(
            [Path(p) for p in input_dict["image_paths"]],
            Dimension.from_dict(input_dict["stitch_dimension"]),
            Dimension.from_dict(input_dict["image_dimension"]),
        )

    def _compute_resolved_paths(self) -> Sequence[str]:
        return [str(p.resolve()) for p in self.image_paths]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "image_paths": self._compute_resolved_paths(),
            "stitch_dimension": self.stitch_dimension.to_dict(),
            "image_dimension": self.image_dimension.to_dict(),
        }
