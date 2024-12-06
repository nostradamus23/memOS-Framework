"""
Configuration module for MemOS AI Framework.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json

from memos.utils.logger import get_logger

class Config:
    """Configuration class for MemOS AI Framework."""

    # Default configuration values
    DEFAULTS = {
        "version": "0.1.0",
        "logging": {
            "level": "INFO",
            "file": "memos.log",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "processing": {
            "image": {
                "target_size": [224, 224],
                "normalize": True,
                "color_mode": "RGB"
            },
            "video": {
                "frame_size": [640, 480],
                "fps": 30,
                "codec": "h264",
                "bitrate": "2M"
            },
            "audio": {
                "sample_rate": 44100,
                "channels": 2,
                "format": "wav"
            },
            "batch_size": 32,
            "num_workers": 4
        },
        "models": {
            "vision": {
                "name": "resnet50",
                "pretrained": True,
                "device": "cuda"
            },
            "text": {
                "name": "gpt2",
                "max_length": 512
            }
        },
        "llm": {
            "openai": {
                "api_key": None,
                "organization": None,
                "default_model": "gpt-4-turbo-preview",
                "temperature": 0.7,
                "max_tokens": 1000
            },
            "anthropic": {
                "api_key": None,
                "default_model": "claude-3-opus",
                "temperature": 0.7,
                "max_tokens": 1000
            },
            "google": {
                "api_key": None,
                "project_id": None,
                "default_model": "gemini-pro",
                "temperature": 0.7,
                "max_tokens": 1000
            },
            "llama": {
                "model_path": None,
                "device": "cuda",
                "context_length": 4096,
                "temperature": 0.7
            }
        },
        "social": {
            "twitter": {
                "api_key": None,
                "api_secret": None,
                "access_token": None,
                "access_token_secret": None,
                "bearer_token": None
            },
            "instagram": {
                "client_id": None,
                "client_secret": None,
                "access_token": None
            },
            "tiktok": {
                "client_key": None,
                "client_secret": None,
                "access_token": None
            },
            "reddit": {
                "client_id": None,
                "client_secret": None,
                "user_agent": None
            }
        },
        "storage": {
            "root_dir": "data",
            "cache_dir": "cache",
            "max_cache_size": 1024,  # MB
            "media_dir": "media",
            "temp_dir": "temp"
        },
        "api": {
            "host": "localhost",
            "port": 8000,
            "debug": False,
            "cors_origins": ["*"],
            "rate_limit": {
                "requests": 100,
                "period": 60  # seconds
            }
        },
        "features": {
            "video_processing": {
                "enabled": True,
                "max_duration": 300,  # seconds
                "supported_formats": ["mp4", "avi", "mov", "webm"],
                "scene_detection": True,
                "motion_analysis": True
            },
            "social_integration": {
                "enabled": True,
                "auto_posting": False,
                "content_moderation": True,
                "engagement_tracking": True
            },
            "llm_integration": {
                "enabled": True,
                "default_provider": "openai",
                "fallback_providers": ["anthropic", "google"],
                "context_window": 4096,
                "streaming": True
            },
            "experimental": {
                "multimodal_fusion": False,
                "real_time_processing": False,
                "distributed_inference": False,
                "federated_learning": False
            }
        },
        "future_integrations": {
            "platforms": [
                "facebook",
                "linkedin",
                "discord",
                "telegram",
                "whatsapp"
            ],
            "features": [
                "live_streaming",
                "ar_filters",
                "3d_memes",
                "voice_synthesis",
                "cross_platform_analytics"
            ],
            "ai_models": [
                "stable_diffusion",
                "midjourney",
                "palm",
                "falcon"
            ]
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration."""
        self.logger = get_logger(__name__)
        self._config = self.DEFAULTS.copy()
        self._update_from_env()
        
        if config_path:
            self._load_from_file(config_path)
        
        self._setup_directories()
        self.logger.info("Configuration initialized successfully")

    def _update_from_env(self) -> None:
        """Update configuration from environment variables."""
        env_prefix = "MEMOS_"
        for key in os.environ:
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                value = os.environ[key]
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass
                self._set_nested_value(config_key.split("_"), value)

    def _load_from_file(self, config_path: str) -> None:
        """Load configuration from file."""
        config_path = Path(config_path)
        if not config_path.exists():
            self.logger.warning(f"Configuration file not found: {config_path}")
            return
        
        try:
            with open(config_path) as f:
                file_config = json.load(f)
            self._update_recursive(self._config, file_config)
            self.logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to load configuration file: {str(e)}")

    def _update_recursive(self, base: Dict, update: Dict) -> None:
        """Recursively update nested dictionary."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._update_recursive(base[key], value)
            else:
                base[key] = value

    def _set_nested_value(self, keys: list, value: Any) -> None:
        """Set value in nested dictionary using key path."""
        current = self._config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def _setup_directories(self) -> None:
        """Create necessary directories."""
        root_dir = Path(self._config["storage"]["root_dir"])
        cache_dir = Path(self._config["storage"]["cache_dir"])
        media_dir = root_dir / self._config["storage"]["media_dir"]
        temp_dir = root_dir / self._config["storage"]["temp_dir"]
        
        for directory in [root_dir, cache_dir, media_dir, temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        try:
            value = self._config
            for k in key.split("."):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._set_nested_value(key.split("."), value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.copy()

    def save(self, config_path: str) -> None:
        """Save configuration to file."""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, "w") as f:
                json.dump(self._config, f, indent=4)
            self.logger.info(f"Saved configuration to {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {str(e)}")

    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access to configuration values."""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Dictionary-style setting of configuration values."""
        self.set(key, value) 