"""
Context - Represents the contextual state and awareness of a meme entity.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

class Context:
    """
    Represents the contextual awareness and state of a meme entity.
    """

    def __init__(self):
        """Initialize a new Context instance."""
        self.creation_time = datetime.now()
        self.last_update = self.creation_time
        
        # Core context attributes
        self._environment: Dict[str, Any] = {}
        self._user_context: Dict[str, Any] = {}
        self._interaction_history: List[Dict[str, Any]] = []
        self._memory: Dict[str, Any] = {}
        self._preferences: Dict[str, Any] = {}
        
    def update_environment(self, env_data: Dict[str, Any]) -> None:
        """
        Update environmental context data.

        Args:
            env_data: Dictionary of environmental context information.
        """
        self._environment.update(env_data)
        self._update_timestamp()

    def update_user_context(self, user_data: Dict[str, Any]) -> None:
        """
        Update user-specific context data.

        Args:
            user_data: Dictionary of user context information.
        """
        self._user_context.update(user_data)
        self._update_timestamp()

    def add_interaction(self, interaction: Dict[str, Any]) -> None:
        """
        Add a new interaction to the history.

        Args:
            interaction: Dictionary containing interaction details.
        """
        interaction["timestamp"] = datetime.now()
        self._interaction_history.append(interaction)
        self._update_timestamp()

    def get_recent_interactions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get recent interactions from history.

        Args:
            limit: Optional limit on number of interactions to return.

        Returns:
            List[Dict[str, Any]]: List of recent interactions.
        """
        if limit is None:
            return self._interaction_history
        return self._interaction_history[-limit:]

    def update_memory(self, key: str, value: Any) -> None:
        """
        Update a memory value.

        Args:
            key: Memory key.
            value: Memory value.
        """
        self._memory[key] = value
        self._update_timestamp()

    def get_memory(self, key: str) -> Optional[Any]:
        """
        Retrieve a memory value.

        Args:
            key: Memory key.

        Returns:
            Optional[Any]: The memory value if it exists.
        """
        return self._memory.get(key)

    def set_preference(self, key: str, value: Any) -> None:
        """
        Set a preference value.

        Args:
            key: Preference key.
            value: Preference value.
        """
        self._preferences[key] = value
        self._update_timestamp()

    def get_preference(self, key: str) -> Optional[Any]:
        """
        Get a preference value.

        Args:
            key: Preference key.

        Returns:
            Optional[Any]: The preference value if it exists.
        """
        return self._preferences.get(key)

    def _update_timestamp(self) -> None:
        """Update the last modification timestamp."""
        self.last_update = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the context to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary representation of the context.
        """
        return {
            "creation_time": self.creation_time.isoformat(),
            "last_update": self.last_update.isoformat(),
            "environment": self._environment,
            "user_context": self._user_context,
            "interaction_history": self._interaction_history,
            "memory": self._memory,
            "preferences": self._preferences
        }

    def __repr__(self) -> str:
        """String representation of the context."""
        return f"Context(created={self.creation_time}, last_update={self.last_update})" 