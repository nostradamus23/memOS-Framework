"""
Basic usage example for MemOS AI Framework.
"""

import sys
from pathlib import Path
import logging

from memos.core import MemOSEngine
from memos.entities import MemeEntity
from memos.config import Config
from memos.utils.logger import get_logger

def main():
    """Main example function."""
    # Setup logging
    logger = get_logger(__name__, level=logging.INFO)
    logger.info("Starting MemOS AI example")
    
    try:
        # Initialize configuration
        config = Config()
        
        # Initialize engine
        engine = MemOSEngine(config)
        logger.info("Initialized MemOS engine")
        
        # Load example meme
        example_path = Path(__file__).parent / "data" / "example_meme.jpg"
        if not example_path.exists():
            logger.error(f"Example meme not found at: {example_path}")
            return 1
        
        # Create meme entity
        entity = MemeEntity.from_image(str(example_path))
        logger.info(f"Created meme entity: {entity.id}")
        
        # Activate entity
        success = engine.activate(entity)
        if not success:
            logger.error("Failed to activate meme entity")
            return 1
        logger.info("Activated meme entity")
        
        # Get initial status
        status = engine.get_entity_status(entity.id)
        logger.info("Initial entity status:")
        logger.info(f"  ID: {status['id']}")
        logger.info(f"  Status: {status['status']}")
        logger.info(f"  Created: {status['creation_time']}")
        
        # Example interaction
        interaction = {
            "type": "text",
            "content": "Hello, meme! How are you feeling today?",
            "metadata": {
                "user": "example_user",
                "timestamp": "2024-01-01T00:00:00"
            }
        }
        
        response = engine.interact(entity.id, interaction)
        logger.info("\nInteraction response:")
        logger.info(f"  Content: {response.get('content', 'No content')}")
        logger.info(f"  Emotion: {response.get('emotion', 'No emotion')}")
        
        # Deactivate entity
        success = engine.deactivate(entity.id)
        if not success:
            logger.error("Failed to deactivate meme entity")
            return 1
        logger.info("Deactivated meme entity")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error in example: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 