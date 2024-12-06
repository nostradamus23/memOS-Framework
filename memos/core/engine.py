"""
MemOS Engine - The core processing unit of the MemOS AI Framework.
"""

import logging
from typing import Optional, List, Dict, Any

from memos.entities import MemeEntity
from memos.core.processor import MemeProcessor
from memos.core.context import ContextManager
from memos.core.emotion import EmotionEngine
from memos.utils.logger import get_logger
from memos.config import Config

class MemOSEngine:
    """
    The main engine class that orchestrates all MemOS AI operations.
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the MemOS Engine.

        Args:
            config: Optional configuration object. If not provided, default config will be used.
        """
        self.config = config or Config()
        self.logger = get_logger(__name__)
        
        # Initialize core components
        self.processor = MemeProcessor(self.config)
        self.context_manager = ContextManager(self.config)
        self.emotion_engine = EmotionEngine(self.config)
        
        self.active_entities: Dict[str, MemeEntity] = {}
        self.logger.info("MemOS Engine initialized successfully")

    def activate(self, meme: MemeEntity) -> bool:
        """
        Activate a meme entity in the MemOS environment.

        Args:
            meme: The meme entity to activate.

        Returns:
            bool: True if activation was successful, False otherwise.
        """
        try:
            # Process the meme
            self.processor.process(meme)
            
            # Initialize context
            context = self.context_manager.create_context(meme)
            meme.set_context(context)
            
            # Initialize emotional state
            emotional_state = self.emotion_engine.initialize_state(meme)
            meme.set_emotional_state(emotional_state)
            
            # Register the active entity
            self.active_entities[meme.id] = meme
            
            self.logger.info(f"Successfully activated meme entity: {meme.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to activate meme entity: {str(e)}")
            return False

    def interact(self, meme_id: str, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an interaction with a meme entity.

        Args:
            meme_id: The ID of the meme to interact with.
            interaction: Dictionary containing interaction details.

        Returns:
            Dict[str, Any]: The response from the meme entity.
        """
        if meme_id not in self.active_entities:
            raise ValueError(f"No active meme entity found with ID: {meme_id}")

        meme = self.active_entities[meme_id]
        
        # Update context based on interaction
        self.context_manager.update_context(meme, interaction)
        
        # Process emotional response
        emotional_response = self.emotion_engine.process_interaction(meme, interaction)
        
        # Generate meme response
        response = self.processor.generate_response(meme, interaction, emotional_response)
        
        return response

    def deactivate(self, meme_id: str) -> bool:
        """
        Deactivate a meme entity.

        Args:
            meme_id: The ID of the meme to deactivate.

        Returns:
            bool: True if deactivation was successful, False otherwise.
        """
        if meme_id in self.active_entities:
            try:
                meme = self.active_entities[meme_id]
                # Cleanup resources
                self.context_manager.cleanup(meme)
                self.emotion_engine.cleanup(meme)
                
                # Remove from active entities
                del self.active_entities[meme_id]
                
                self.logger.info(f"Successfully deactivated meme entity: {meme_id}")
                return True
            except Exception as e:
                self.logger.error(f"Error deactivating meme entity: {str(e)}")
                return False
        return False

    def get_active_entities(self) -> List[str]:
        """
        Get a list of all active meme entity IDs.

        Returns:
            List[str]: List of active meme entity IDs.
        """
        return list(self.active_entities.keys())

    def get_entity_status(self, meme_id: str) -> Dict[str, Any]:
        """
        Get the current status of a meme entity.

        Args:
            meme_id: The ID of the meme entity.

        Returns:
            Dict[str, Any]: Dictionary containing entity status information.
        """
        if meme_id not in self.active_entities:
            raise ValueError(f"No active meme entity found with ID: {meme_id}")

        meme = self.active_entities[meme_id]
        return {
            "id": meme.id,
            "status": "active",
            "context": meme.get_context(),
            "emotional_state": meme.get_emotional_state(),
            "creation_time": meme.creation_time,
            "last_interaction": meme.last_interaction_time
        } 