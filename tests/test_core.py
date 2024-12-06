"""
Tests for core MemOS AI functionality.
"""

import pytest
import numpy as np
from pathlib import Path

from memos.core import MemOSEngine
from memos.entities import MemeEntity
from memos.config import Config

@pytest.fixture
def config():
    """Fixture for test configuration."""
    return Config()

@pytest.fixture
def engine(config):
    """Fixture for MemOS engine."""
    return MemOSEngine(config)

@pytest.fixture
def sample_image():
    """Fixture for sample image data."""
    return np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

def test_engine_initialization(engine):
    """Test engine initialization."""
    assert engine is not None
    assert isinstance(engine, MemOSEngine)

def test_meme_entity_creation(sample_image):
    """Test meme entity creation."""
    entity = MemeEntity.from_array(sample_image)
    assert entity is not None
    assert entity.id is not None
    assert entity.image_data is not None

def test_meme_activation(engine, sample_image):
    """Test meme activation."""
    entity = MemeEntity.from_array(sample_image)
    success = engine.activate(entity)
    assert success
    assert entity.id in engine.get_active_entities()

def test_meme_interaction(engine, sample_image):
    """Test meme interaction."""
    entity = MemeEntity.from_array(sample_image)
    engine.activate(entity)
    
    interaction = {
        "type": "text",
        "content": "Hello, meme!",
        "timestamp": "2024-01-01T00:00:00"
    }
    
    response = engine.interact(entity.id, interaction)
    assert response is not None

def test_meme_deactivation(engine, sample_image):
    """Test meme deactivation."""
    entity = MemeEntity.from_array(sample_image)
    engine.activate(entity)
    
    success = engine.deactivate(entity.id)
    assert success
    assert entity.id not in engine.get_active_entities()

def test_entity_status(engine, sample_image):
    """Test entity status retrieval."""
    entity = MemeEntity.from_array(sample_image)
    engine.activate(entity)
    
    status = engine.get_entity_status(entity.id)
    assert status is not None
    assert status["id"] == entity.id
    assert status["status"] == "active"

def test_invalid_entity_id(engine):
    """Test handling of invalid entity ID."""
    with pytest.raises(ValueError):
        engine.get_entity_status("invalid_id")

def test_multiple_entities(engine, sample_image):
    """Test handling multiple entities."""
    entities = [
        MemeEntity.from_array(sample_image),
        MemeEntity.from_array(sample_image),
        MemeEntity.from_array(sample_image)
    ]
    
    # Activate all entities
    for entity in entities:
        success = engine.activate(entity)
        assert success
    
    # Check all entities are active
    active_ids = engine.get_active_entities()
    assert len(active_ids) == len(entities)
    for entity in entities:
        assert entity.id in active_ids
    
    # Deactivate all entities
    for entity in entities:
        success = engine.deactivate(entity.id)
        assert success
    
    # Check all entities are deactivated
    assert len(engine.get_active_entities()) == 0 