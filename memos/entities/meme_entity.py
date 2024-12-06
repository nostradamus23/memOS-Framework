"""
MemeEntity - The core entity class representing an interactive meme in the MemOS environment.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

import numpy as np
from PIL import Image

from memos.entities.context import Context
from memos.entities.emotional_state import EmotionalState
from memos.utils.image_processing import load_image, preprocess_image
from memos.utils.logger import get_logger

class MemeEntity:
    """
    Represents a meme as an interactive entity within the MemOS environment.
    """

    def __init__(self, 
                 image_path: Optional[str] = None, 
                 image_data: Optional[np.ndarray] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a new MemeEntity.

        Args:
            image_path: Path to the meme image file.
            image_data: Raw image data as numpy array.
            metadata: Additional metadata about the meme.
        """
        if not image_path and image_data is None:
            raise ValueError("Either image_path or image_data must be provided")

        self.id = str(uuid.uuid4())
        self.logger = get_logger(__name__)
        
        # Image data
        self.image_path = image_path
        self.image_data = image_data
        if image_path:
            self.image_data = load_image(image_path)
        
        # Metadata
        self.metadata = metadata or {}
        self.creation_time = datetime.now()
        self.last_interaction_time: Optional[datetime] = None
        
        # State
        self._context: Optional[Context] = None
        self._emotional_state: Optional[EmotionalState] = None
        self._features: Dict[str, Any] = {}
        
        self.logger.info(f"Created new MemeEntity with ID: {self.id}")

    @classmethod
    def from_image(cls, image_path: str) -> 'MemeEntity':
        """
        Create a MemeEntity from an image file.

        Args:
            image_path: Path to the image file.

        Returns:
            MemeEntity: A new meme entity instance.
        """
        return cls(image_path=image_path)

    @classmethod
    def from_array(cls, image_data: np.ndarray, metadata: Optional[Dict[str, Any]] = None) -> 'MemeEntity':
        """
        Create a MemeEntity from a numpy array.

        Args:
            image_data: Image data as numpy array.
            metadata: Optional metadata about the meme.

        Returns:
            MemeEntity: A new meme entity instance.
        """
        return cls(image_data=image_data, metadata=metadata)

    def set_context(self, context: Context) -> None:
        """
        Set the context for this meme entity.

        Args:
            context: The context object to set.
        """
        self._context = context
        self.logger.debug(f"Updated context for entity {self.id}")

    def get_context(self) -> Optional[Context]:
        """
        Get the current context of the meme entity.

        Returns:
            Optional[Context]: The current context or None if not set.
        """
        return self._context

    def set_emotional_state(self, state: EmotionalState) -> None:
        """
        Set the emotional state for this meme entity.

        Args:
            state: The emotional state to set.
        """
        self._emotional_state = state
        self.logger.debug(f"Updated emotional state for entity {self.id}")

    def get_emotional_state(self) -> Optional[EmotionalState]:
        """
        Get the current emotional state of the meme entity.

        Returns:
            Optional[EmotionalState]: The current emotional state or None if not set.
        """
        return self._emotional_state

    def update_features(self, features: Dict[str, Any]) -> None:
        """
        Update the extracted features of the meme.

        Args:
            features: Dictionary of extracted features.
        """
        self._features.update(features)
        self.logger.debug(f"Updated features for entity {self.id}")

    def get_features(self) -> Dict[str, Any]:
        """
        Get the extracted features of the meme.

        Returns:
            Dict[str, Any]: Dictionary of extracted features.
        """
        return self._features

    def record_interaction(self) -> None:
        """Record the timestamp of the latest interaction."""
        self.last_interaction_time = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entity to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary representation of the entity.
        """
        return {
            "id": self.id,
            "creation_time": self.creation_time.isoformat(),
            "last_interaction_time": self.last_interaction_time.isoformat() if self.last_interaction_time else None,
            "metadata": self.metadata,
            "context": self._context.to_dict() if self._context else None,
            "emotional_state": self._emotional_state.to_dict() if self._emotional_state else None,
            "features": self._features
        }

    def __repr__(self) -> str:
        """String representation of the entity."""
        return f"MemeEntity(id={self.id}, created={self.creation_time})" 