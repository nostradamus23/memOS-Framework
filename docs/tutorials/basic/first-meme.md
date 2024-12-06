# Creating Your First Meme Entity

This tutorial will guide you through the process of creating and interacting with your first meme entity using the MemOS AI Framework.

## Prerequisites

- Python 3.8 or higher
- MemOS AI Framework installed
- Basic understanding of Python async/await
- A meme image file

## Table of Contents

1. [Installation](#installation)
2. [Basic Setup](#basic-setup)
3. [Creating a Meme Entity](#creating-a-meme-entity)
4. [Adding Context](#adding-context)
5. [Emotional Processing](#emotional-processing)
6. [Interaction Flow](#interaction-flow)
7. [Advanced Features](#advanced-features)

## Installation

First, install the MemOS AI Framework:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install MemOS AI
pip install memos-ai
```

## Basic Setup

Create a new Python file `first_meme.py`:

```python
import asyncio
from pathlib import Path
from memos import MemOSEngine, Config
from memos.entities import MemeEntity

async def main():
    # Initialize configuration
    config = Config()
    
    # Create engine instance
    engine = MemOSEngine(config)
    
    # Path to your meme image
    meme_path = Path("path/to/your/meme.jpg")
    
    # Create entity
    entity = await create_meme_entity(engine, meme_path)
    
    # Interact with entity
    await interact_with_entity(engine, entity)

async def create_meme_entity(engine, image_path):
    print(f"Creating meme entity from: {image_path}")
    return await engine.create_entity(image_path)

async def interact_with_entity(engine, entity):
    print(f"Starting interaction with entity: {entity.id}")
    # We'll add interaction code here

if __name__ == "__main__":
    asyncio.run(main())
```

## Creating a Meme Entity

Let's expand the `create_meme_entity` function:

```python
async def create_meme_entity(engine, image_path):
    # Create basic entity
    entity = MemeEntity.from_image(str(image_path))
    
    # Add initial metadata
    entity.metadata.update({
        "creator": "tutorial_user",
        "creation_time": datetime.now().isoformat(),
        "source": "tutorial",
        "tags": ["tutorial", "first_meme"]
    })
    
    # Initialize context
    context = {
        "environment": {
            "platform": "tutorial",
            "version": "1.0.0"
        },
        "user_context": {
            "experience_level": "beginner",
            "interaction_count": 0
        }
    }
    entity.set_context(context)
    
    # Activate entity
    success = await engine.activate(entity)
    if not success:
        raise RuntimeError("Failed to activate entity")
    
    print(f"Created entity: {entity.id}")
    return entity
```

## Adding Context

Expand the entity with contextual awareness:

```python
async def add_context(entity):
    # Create context manager
    context_manager = entity.get_context_manager()
    
    # Add environmental context
    await context_manager.update_environment({
        "time_of_day": get_time_of_day(),
        "platform": sys.platform,
        "language": "en"
    })
    
    # Add user preferences
    await context_manager.set_preference(
        "response_style",
        "humorous"
    )
    
    # Add memory
    await context_manager.update_memory(
        "creation_info",
        {
            "created_at": datetime.now(),
            "purpose": "tutorial"
        }
    )

def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:
        return "night"
```

## Emotional Processing

Add emotional intelligence to your entity:

```python
async def setup_emotions(entity):
    # Get emotion engine
    emotion_engine = entity.get_emotion_engine()
    
    # Set initial emotional state
    await emotion_engine.update_emotion("joy", 0.7)
    await emotion_engine.update_emotion("interest", 0.8)
    
    # Add personality traits
    await emotion_engine.set_personality_trait("openness", 0.9)
    await emotion_engine.set_personality_trait("humor", 0.8)
    
    # Configure response patterns
    await emotion_engine.configure_responses({
        "greeting": {
            "joy": "Enthusiastic welcome",
            "neutral": "Standard greeting",
            "low_energy": "Calm acknowledgment"
        },
        "farewell": {
            "joy": "Excited goodbye",
            "neutral": "Standard farewell",
            "low_energy": "Subtle departure"
        }
    })
```

## Interaction Flow

Now let's implement the interaction logic:

```python
async def interact_with_entity(engine, entity):
    # Create interaction loop
    while True:
        # Get user input
        user_input = await get_user_input()
        if user_input.lower() == "exit":
            break
        
        # Create interaction
        interaction = {
            "type": "text",
            "content": user_input,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "source": "tutorial",
                "session_id": str(uuid.uuid4())
            }
        }
        
        # Process interaction
        response = await engine.process_interaction(
            entity.id,
            interaction
        )
        
        # Display response
        print_response(response)
        
        # Update interaction count
        context = entity.get_context()
        context.user_context["interaction_count"] += 1

async def get_user_input():
    return input("You: ")

def print_response(response):
    print(f"\nMeme: {response['content']}")
    if "emotion" in response:
        print(f"Emotion: {response['emotion']}")
    print()
```

## Advanced Features

Let's add some advanced features:

```python
class AdvancedMemeEntity:
    def __init__(self, base_entity):
        self.entity = base_entity
        self.interaction_history = []
        self.state_manager = StateManager()
        self.feature_extractor = FeatureExtractor()
    
    async def process_interaction(self, interaction):
        # Extract features
        features = await self.feature_extractor.extract(
            interaction
        )
        
        # Update state
        await self.state_manager.update(features)
        
        # Get response
        response = await self.entity.generate_response(
            interaction,
            features=features,
            state=self.state_manager.current_state
        )
        
        # Record interaction
        self.interaction_history.append({
            "interaction": interaction,
            "features": features,
            "response": response,
            "timestamp": datetime.now()
        })
        
        return response
    
    async def analyze_interaction_history(self):
        return {
            "total_interactions": len(self.interaction_history),
            "average_sentiment": await self.calculate_average_sentiment(),
            "common_topics": await self.extract_common_topics(),
            "interaction_patterns": await self.analyze_patterns()
        }
    
    async def calculate_average_sentiment(self):
        if not self.interaction_history:
            return 0.0
        
        total = sum(
            interaction["features"].get("sentiment", 0)
            for interaction in self.interaction_history
        )
        return total / len(self.interaction_history)
    
    async def extract_common_topics(self):
        topics = {}
        for interaction in self.interaction_history:
            for topic in interaction["features"].get("topics", []):
                topics[topic] = topics.get(topic, 0) + 1
        
        return sorted(
            topics.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
    
    async def analyze_patterns(self):
        return {
            "time_patterns": self.analyze_time_patterns(),
            "response_patterns": self.analyze_response_patterns(),
            "emotional_patterns": self.analyze_emotional_patterns()
        }
```

## Complete Example

Here's a complete example putting it all together:

```python
async def main():
    # Initialize
    config = Config()
    engine = MemOSEngine(config)
    
    # Create entity
    entity = await create_meme_entity(
        engine,
        Path("meme.jpg")
    )
    
    # Add context and emotions
    await add_context(entity)
    await setup_emotions(entity)
    
    # Create advanced entity
    advanced_entity = AdvancedMemeEntity(entity)
    
    # Start interaction loop
    try:
        await interact_with_entity(engine, advanced_entity)
    finally:
        # Analysis
        analysis = await advanced_entity.analyze_interaction_history()
        print("\nInteraction Analysis:")
        print(json.dumps(analysis, indent=2))
        
        # Cleanup
        await engine.deactivate(entity.id)

if __name__ == "__main__":
    asyncio.run(main())
```

## Next Steps

Now that you've created your first meme entity, you can:

1. Experiment with different context types
2. Implement custom emotional responses
3. Add more advanced features
4. Integrate with external services
5. Implement persistence
6. Add error handling and logging

For more advanced topics, check out:
- [Advanced Context Management](../advanced/context-management.md)
- [Complex Interaction Patterns](../advanced/interaction-patterns.md)
- [State Synchronization](../advanced/state-sync.md)
- [Integration Tutorials](../integration/index.md) 