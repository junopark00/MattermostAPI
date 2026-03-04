"""
Mattermost data model base module.

Defines the base class providing common functionality for all models.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any, Optional, TypeVar

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    """
    Base class for all Mattermost data models.

    Provides common factory methods for converting API response JSON
    to Python dataclasses, plus serialization utilities.
    """

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """
        Create a model instance from a dictionary.
        Keys not defined on the model are silently ignored.

        Args:
            data: API response JSON dictionary.

        Returns:
            Model instance.
        """
        valid_fields = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

    def to_dict(self, exclude_none: bool = False) -> dict[str, Any]:
        """
        Convert the model to a dictionary.

        Args:
            exclude_none: If True, exclude fields with None values.

        Returns:
            Dictionary of model fields and values.
        """
        result = asdict(self)
        if exclude_none:
            result = {k: v for k, v in result.items() if v is not None}
        return result

    @classmethod
    def from_list(cls: type[T], data_list: list[dict[str, Any]]) -> list[T]:
        """
        Create a list of model instances from a list of dictionaries.

        Args:
            data_list: List of API response JSON dictionaries.

        Returns:
            List of model instances.
        """
        return [cls.from_dict(item) for item in data_list]
