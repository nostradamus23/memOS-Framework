"""
API module for MemOS AI Framework.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import tempfile
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import uvicorn

from memos.core import MemOSEngine
from memos.entities import MemeEntity
from memos.config import Config
from memos.utils.logger import get_logger

# Initialize FastAPI app
app = FastAPI(
    title="MemOS AI API",
    description="API for transforming static memes into interactive digital entities",
    version="0.1.0"
)

# Initialize global components
config = Config()
engine = MemOSEngine(config)
logger = get_logger(__name__)

# Pydantic models for request/response
class InteractionRequest(BaseModel):
    """Model for interaction requests."""
    type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class InteractionResponse(BaseModel):
    """Model for interaction responses."""
    entity_id: str
    response: Dict[str, Any]
    status: str

class EntityStatus(BaseModel):
    """Model for entity status."""
    id: str
    status: str
    creation_time: str
    last_interaction_time: Optional[str] = None
    metadata: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MemOS AI API",
        "version": "0.1.0",
        "status": "active"
    }

@app.post("/memes/upload", response_model=EntityStatus)
async def upload_meme(file: UploadFile = File(...)):
    """
    Upload and process a new meme image.
    
    Args:
        file: Uploaded image file.
    
    Returns:
        EntityStatus: Status of the created entity.
    """
    try:
        # Create temporary file
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Create and activate entity
        entity = MemeEntity.from_image(temp_path)
        success = engine.activate(entity)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to activate meme entity")
        
        # Get entity status
        status = engine.get_entity_status(entity.id)
        
        # Clean up temporary file
        Path(temp_path).unlink()
        
        return status
        
    except Exception as e:
        logger.error(f"Failed to process uploaded meme: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memes/{entity_id}/interact", response_model=InteractionResponse)
async def interact_with_meme(entity_id: str, interaction: InteractionRequest):
    """
    Interact with a meme entity.
    
    Args:
        entity_id: ID of the target entity.
        interaction: Interaction details.
    
    Returns:
        InteractionResponse: Response from the entity.
    """
    try:
        # Validate entity exists
        if entity_id not in engine.get_active_entities():
            raise HTTPException(status_code=404, detail="Entity not found")
        
        # Process interaction
        response = engine.interact(entity_id, interaction.dict())
        
        return InteractionResponse(
            entity_id=entity_id,
            response=response,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Failed to process interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memes/{entity_id}", response_model=EntityStatus)
async def get_meme_status(entity_id: str):
    """
    Get status of a meme entity.
    
    Args:
        entity_id: ID of the target entity.
    
    Returns:
        EntityStatus: Current status of the entity.
    """
    try:
        return engine.get_entity_status(entity_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Entity not found")
    except Exception as e:
        logger.error(f"Failed to get entity status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memes", response_model=List[EntityStatus])
async def list_memes():
    """
    List all active meme entities.
    
    Returns:
        List[EntityStatus]: List of active entity statuses.
    """
    try:
        active_ids = engine.get_active_entities()
        return [
            engine.get_entity_status(entity_id)
            for entity_id in active_ids
        ]
    except Exception as e:
        logger.error(f"Failed to list entities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memes/{entity_id}")
async def deactivate_meme(entity_id: str):
    """
    Deactivate a meme entity.
    
    Args:
        entity_id: ID of the target entity.
    
    Returns:
        dict: Deactivation status.
    """
    try:
        success = engine.deactivate(entity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        return {"status": "success", "message": f"Entity {entity_id} deactivated"}
        
    except Exception as e:
        logger.error(f"Failed to deactivate entity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def start_server(host: str = "localhost", 
                port: int = 8000, 
                reload: bool = False) -> None:
    """
    Start the API server.
    
    Args:
        host: Host address to bind to.
        port: Port number to listen on.
        reload: Whether to enable auto-reload.
    """
    uvicorn.run(
        "memos.api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    ) 