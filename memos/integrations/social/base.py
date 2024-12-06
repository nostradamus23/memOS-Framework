"""
Base classes for social media integrations in MemOS AI Framework.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MediaType(Enum):
    """Types of media content."""
    IMAGE = "image"
    VIDEO = "video"
    GIF = "gif"
    TEXT = "text"
    AUDIO = "audio"
    MIXED = "mixed"

@dataclass
class MediaContent:
    """Container for media content."""
    type: MediaType
    url: Optional[str] = None
    data: Optional[bytes] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class SocialPost:
    """Container for social media posts."""
    platform: str
    content: str
    media: Optional[List[MediaContent]] = None
    timestamp: datetime = datetime.now()
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Engagement:
    """Container for engagement metrics."""
    likes: int = 0
    shares: int = 0
    comments: int = 0
    views: int = 0
    metadata: Optional[Dict[str, Any]] = None

class SocialPlatform(ABC):
    """Base class for social media platform integrations."""

    def __init__(self,
                 credentials: Dict[str, str],
                 **kwargs):
        """
        Initialize social platform integration.

        Args:
            credentials: Platform-specific credentials.
            **kwargs: Additional platform-specific arguments.
        """
        self.credentials = credentials
        self.kwargs = kwargs
        self._validate_credentials()

    @abstractmethod
    def _validate_credentials(self) -> None:
        """Validate platform credentials."""
        pass

    @abstractmethod
    async def post(self,
                  content: str,
                  media: Optional[List[MediaContent]] = None,
                  **kwargs) -> SocialPost:
        """
        Create a new post.

        Args:
            content: Post text content.
            media: Optional media attachments.
            **kwargs: Additional platform-specific arguments.

        Returns:
            SocialPost: Created post details.
        """
        pass

    @abstractmethod
    async def delete_post(self, post_id: str) -> bool:
        """
        Delete a post.

        Args:
            post_id: ID of the post to delete.

        Returns:
            bool: True if deletion was successful.
        """
        pass

    @abstractmethod
    async def get_engagement(self, post_id: str) -> Engagement:
        """
        Get engagement metrics for a post.

        Args:
            post_id: ID of the post.

        Returns:
            Engagement: Engagement metrics.
        """
        pass

    @abstractmethod
    async def get_comments(self,
                         post_id: str,
                         limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get comments on a post.

        Args:
            post_id: ID of the post.
            limit: Optional limit on number of comments.

        Returns:
            List[Dict[str, Any]]: List of comments.
        """
        pass

    @abstractmethod
    async def reply_to_comment(self,
                             post_id: str,
                             comment_id: str,
                             content: str,
                             media: Optional[List[MediaContent]] = None) -> Dict[str, Any]:
        """
        Reply to a comment.

        Args:
            post_id: ID of the parent post.
            comment_id: ID of the comment to reply to.
            content: Reply text content.
            media: Optional media attachments.

        Returns:
            Dict[str, Any]: Reply details.
        """
        pass

    @abstractmethod
    async def get_analytics(self,
                          post_id: str,
                          metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get detailed analytics for a post.

        Args:
            post_id: ID of the post.
            metrics: Optional list of specific metrics to retrieve.

        Returns:
            Dict[str, Any]: Analytics data.
        """
        pass

    @abstractmethod
    async def schedule_post(self,
                          content: str,
                          schedule_time: datetime,
                          media: Optional[List[MediaContent]] = None,
                          **kwargs) -> Dict[str, Any]:
        """
        Schedule a post for later.

        Args:
            content: Post text content.
            schedule_time: When to publish the post.
            media: Optional media attachments.
            **kwargs: Additional platform-specific arguments.

        Returns:
            Dict[str, Any]: Scheduled post details.
        """
        pass

    @abstractmethod
    def validate_media(self, media: List[MediaContent]) -> bool:
        """
        Validate media content for platform compatibility.

        Args:
            media: List of media content to validate.

        Returns:
            bool: True if all media is valid.
        """
        pass

class SocialException(Exception):
    """Base exception for social media-related errors."""
    pass

class InvalidCredentials(SocialException):
    """Exception for invalid credentials."""
    pass

class MediaValidationError(SocialException):
    """Exception for invalid media content."""
    pass

class RateLimitExceeded(SocialException):
    """Exception for rate limit violations."""
    pass

class ContentModerationError(SocialException):
    """Exception for content that violates platform policies."""
    pass 