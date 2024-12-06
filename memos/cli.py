"""
Command-line interface for MemOS AI Framework.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from memos.core import MemOSEngine
from memos.entities import MemeEntity
from memos.config import Config
from memos.utils.logger import get_logger

def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="MemOS AI - Transform static memes into interactive digital entities"
    )
    
    # Global options
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Initialize command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new MemOS project"
    )
    init_parser.add_argument(
        "project_path",
        type=str,
        help="Path to create new project"
    )
    
    # Process command
    process_parser = subparsers.add_parser(
        "process",
        help="Process a meme image"
    )
    process_parser.add_argument(
        "image_path",
        type=str,
        help="Path to meme image"
    )
    process_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output path for processed results"
    )
    
    # Interact command
    interact_parser = subparsers.add_parser(
        "interact",
        help="Interact with a meme entity"
    )
    interact_parser.add_argument(
        "entity_id",
        type=str,
        help="ID of the meme entity"
    )
    interact_parser.add_argument(
        "message",
        type=str,
        help="Interaction message"
    )
    
    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List active meme entities"
    )
    
    return parser

def init_project(args: argparse.Namespace, logger: logging.Logger) -> int:
    """
    Initialize a new MemOS project.

    Args:
        args: Command-line arguments.
        logger: Logger instance.

    Returns:
        int: Exit code.
    """
    project_path = Path(args.project_path)
    
    try:
        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create default configuration
        config = Config()
        config.save(project_path / "config.json")
        
        # Create directory structure
        (project_path / "data").mkdir(exist_ok=True)
        (project_path / "cache").mkdir(exist_ok=True)
        (project_path / "logs").mkdir(exist_ok=True)
        
        logger.info(f"Initialized new MemOS project at {project_path}")
        return 0
        
    except Exception as e:
        logger.error(f"Failed to initialize project: {str(e)}")
        return 1

def process_meme(args: argparse.Namespace, logger: logging.Logger) -> int:
    """
    Process a meme image.

    Args:
        args: Command-line arguments.
        logger: Logger instance.

    Returns:
        int: Exit code.
    """
    try:
        # Load configuration
        config = Config(args.config)
        
        # Initialize engine
        engine = MemOSEngine(config)
        
        # Create meme entity
        entity = MemeEntity.from_image(args.image_path)
        
        # Activate entity
        success = engine.activate(entity)
        if not success:
            logger.error("Failed to activate meme entity")
            return 1
        
        # Get entity status
        status = engine.get_entity_status(entity.id)
        
        # Save results if output path specified
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            import json
            with open(output_path, "w") as f:
                json.dump(status, f, indent=4)
        
        logger.info(f"Successfully processed meme: {entity.id}")
        return 0
        
    except Exception as e:
        logger.error(f"Failed to process meme: {str(e)}")
        return 1

def interact_with_meme(args: argparse.Namespace, logger: logging.Logger) -> int:
    """
    Interact with a meme entity.

    Args:
        args: Command-line arguments.
        logger: Logger instance.

    Returns:
        int: Exit code.
    """
    try:
        # Load configuration
        config = Config(args.config)
        
        # Initialize engine
        engine = MemOSEngine(config)
        
        # Create interaction
        interaction = {
            "type": "text",
            "content": args.message
        }
        
        # Send interaction
        response = engine.interact(args.entity_id, interaction)
        
        # Print response
        print(response)
        return 0
        
    except Exception as e:
        logger.error(f"Failed to interact with meme: {str(e)}")
        return 1

def list_entities(args: argparse.Namespace, logger: logging.Logger) -> int:
    """
    List active meme entities.

    Args:
        args: Command-line arguments.
        logger: Logger instance.

    Returns:
        int: Exit code.
    """
    try:
        # Load configuration
        config = Config(args.config)
        
        # Initialize engine
        engine = MemOSEngine(config)
        
        # Get active entities
        active_ids = engine.get_active_entities()
        
        # Print entity information
        print(f"\nActive Meme Entities ({len(active_ids)}):")
        print("-" * 40)
        
        for entity_id in active_ids:
            status = engine.get_entity_status(entity_id)
            print(f"ID: {status['id']}")
            print(f"Status: {status['status']}")
            print(f"Created: {status['creation_time']}")
            print("-" * 40)
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to list entities: {str(e)}")
        return 1

def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        argv: Optional list of command-line arguments.

    Returns:
        int: Exit code.
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = get_logger(__name__, level=log_level)
    
    # Execute command
    if args.command == "init":
        return init_project(args, logger)
    elif args.command == "process":
        return process_meme(args, logger)
    elif args.command == "interact":
        return interact_with_meme(args, logger)
    elif args.command == "list":
        return list_entities(args, logger)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 