"""
EmotionalState - Represents the emotional state and awareness of a meme entity.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np

class EmotionalState:
    """
    Represents the emotional state and awareness of a meme entity.
    """

    # Define core emotions and their default intensities
    CORE_EMOTIONS = {
        "joy": 0.0,
        "sadness": 0.0,
        "anger": 0.0,
        "fear": 0.0,
        "surprise": 0.0,
        "disgust": 0.0,
        "trust": 0.0,
        "anticipation": 0.0
    }

    def __init__(self):
        """Initialize a new EmotionalState instance."""
        self.creation_time = datetime.now()
        self.last_update = self.creation_time
        
        # Core emotional attributes
        self._emotions = self.CORE_EMOTIONS.copy()
        self._mood = 0.0  # Range: -1.0 to 1.0
        self._emotional_history: List[Dict[str, Any]] = []
        self._personality_traits: Dict[str, float] = {}
        
    def update_emotion(self, emotion: str, intensity: float) -> None:
        """
        Update the intensity of a specific emotion.

        Args:
            emotion: Name of the emotion.
            intensity: New intensity value (0.0 to 1.0).
        """
        if emotion not in self._emotions:
            raise ValueError(f"Unknown emotion: {emotion}")
        
        intensity = np.clip(intensity, 0.0, 1.0)
        self._emotions[emotion] = intensity
        self._update_mood()
        self._record_emotional_state()
        self._update_timestamp()

    def get_emotion(self, emotion: str) -> float:
        """
        Get the current intensity of a specific emotion.

        Args:
            emotion: Name of the emotion.

        Returns:
            float: Current intensity of the emotion (0.0 to 1.0).
        """
        if emotion not in self._emotions:
            raise ValueError(f"Unknown emotion: {emotion}")
        return self._emotions[emotion]

    def get_dominant_emotion(self) -> tuple[str, float]:
        """
        Get the currently dominant emotion.

        Returns:
            tuple[str, float]: Tuple of (emotion_name, intensity).
        """
        return max(self._emotions.items(), key=lambda x: x[1])

    def set_mood(self, mood: float) -> None:
        """
        Set the current mood value.

        Args:
            mood: Mood value (-1.0 to 1.0).
        """
        self._mood = np.clip(mood, -1.0, 1.0)
        self._record_emotional_state()
        self._update_timestamp()

    def get_mood(self) -> float:
        """
        Get the current mood value.

        Returns:
            float: Current mood value (-1.0 to 1.0).
        """
        return self._mood

    def set_personality_trait(self, trait: str, value: float) -> None:
        """
        Set a personality trait value.

        Args:
            trait: Name of the personality trait.
            value: Trait value (0.0 to 1.0).
        """
        self._personality_traits[trait] = np.clip(value, 0.0, 1.0)
        self._update_timestamp()

    def get_personality_trait(self, trait: str) -> Optional[float]:
        """
        Get a personality trait value.

        Args:
            trait: Name of the personality trait.

        Returns:
            Optional[float]: Trait value if it exists.
        """
        return self._personality_traits.get(trait)

    def get_emotional_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get emotional state history.

        Args:
            limit: Optional limit on number of records to return.

        Returns:
            List[Dict[str, Any]]: List of emotional state records.
        """
        if limit is None:
            return self._emotional_history
        return self._emotional_history[-limit:]

    def _update_mood(self) -> None:
        """Update the mood based on current emotions."""
        # Simple mood calculation based on weighted average of emotions
        positive_emotions = ["joy", "trust", "anticipation"]
        negative_emotions = ["sadness", "anger", "fear", "disgust"]
        
        positive_value = sum(self._emotions[e] for e in positive_emotions) / len(positive_emotions)
        negative_value = sum(self._emotions[e] for e in negative_emotions) / len(negative_emotions)
        
        self._mood = np.clip(positive_value - negative_value, -1.0, 1.0)

    def _record_emotional_state(self) -> None:
        """Record the current emotional state in history."""
        state = {
            "timestamp": datetime.now(),
            "emotions": self._emotions.copy(),
            "mood": self._mood
        }
        self._emotional_history.append(state)

    def _update_timestamp(self) -> None:
        """Update the last modification timestamp."""
        self.last_update = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the emotional state to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary representation of the emotional state.
        """
        return {
            "creation_time": self.creation_time.isoformat(),
            "last_update": self.last_update.isoformat(),
            "emotions": self._emotions,
            "mood": self._mood,
            "personality_traits": self._personality_traits,
            "emotional_history": [
                {
                    "timestamp": state["timestamp"].isoformat(),
                    "emotions": state["emotions"],
                    "mood": state["mood"]
                }
                for state in self._emotional_history
            ]
        }

    def __repr__(self) -> str:
        """String representation of the emotional state."""
        dominant_emotion, intensity = self.get_dominant_emotion()
        return f"EmotionalState(mood={self._mood:.2f}, dominant_emotion={dominant_emotion}={intensity:.2f})" 