"""
Video processing module for MemOS AI Framework.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional, List, Tuple, Generator
from pathlib import Path
from dataclasses import dataclass
from datetime import timedelta

@dataclass
class VideoMetadata:
    """Container for video metadata."""
    width: int
    height: int
    fps: float
    total_frames: int
    duration: timedelta
    codec: str
    format: str
    bitrate: int
    has_audio: bool
    audio_channels: Optional[int] = None
    audio_sample_rate: Optional[int] = None

@dataclass
class VideoFrame:
    """Container for video frames."""
    frame: np.ndarray
    timestamp: timedelta
    frame_number: int
    metadata: Optional[Dict[str, Any]] = None

class VideoProcessor:
    """Video processing functionality."""

    def __init__(self, video_path: str):
        """
        Initialize video processor.

        Args:
            video_path: Path to video file.
        """
        self.video_path = Path(video_path)
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.cap = cv2.VideoCapture(str(video_path))
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open video: {video_path}")
        
        self.metadata = self._extract_metadata()

    def _extract_metadata(self) -> VideoMetadata:
        """Extract video metadata."""
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = timedelta(seconds=total_frames/fps)
        
        # Get codec information
        fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        
        return VideoMetadata(
            width=width,
            height=height,
            fps=fps,
            total_frames=total_frames,
            duration=duration,
            codec=codec,
            format=self.video_path.suffix[1:],
            bitrate=0,  # Requires additional processing
            has_audio=False,  # Requires additional processing
            audio_channels=None,
            audio_sample_rate=None
        )

    def read_frame(self) -> Optional[VideoFrame]:
        """
        Read next frame from video.

        Returns:
            Optional[VideoFrame]: Next frame or None if end of video.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        timestamp = timedelta(seconds=frame_number/self.metadata.fps)
        
        return VideoFrame(
            frame=frame,
            timestamp=timestamp,
            frame_number=frame_number
        )

    def read_frames(self, start_time: Optional[float] = None,
                   end_time: Optional[float] = None) -> Generator[VideoFrame, None, None]:
        """
        Read frames within time range.

        Args:
            start_time: Optional start time in seconds.
            end_time: Optional end time in seconds.

        Yields:
            VideoFrame: Video frames.
        """
        if start_time is not None:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
        
        while True:
            frame = self.read_frame()
            if frame is None:
                break
            
            if end_time is not None and frame.timestamp.total_seconds() > end_time:
                break
            
            yield frame

    def extract_keyframes(self, threshold: float = 0.5) -> List[VideoFrame]:
        """
        Extract key frames from video.

        Args:
            threshold: Difference threshold for key frame detection.

        Returns:
            List[VideoFrame]: List of key frames.
        """
        keyframes = []
        prev_frame = None
        
        while True:
            frame = self.read_frame()
            if frame is None:
                break
            
            if prev_frame is None:
                keyframes.append(frame)
                prev_frame = frame.frame
                continue
            
            # Calculate frame difference
            diff = np.mean(cv2.absdiff(frame.frame, prev_frame))
            if diff > threshold:
                keyframes.append(frame)
                prev_frame = frame.frame
        
        return keyframes

    def extract_scene_changes(self, threshold: float = 30.0) -> List[Tuple[timedelta, timedelta]]:
        """
        Detect scene changes in video.

        Args:
            threshold: Threshold for scene change detection.

        Returns:
            List[Tuple[timedelta, timedelta]]: List of scene intervals.
        """
        scenes = []
        scene_start = timedelta()
        prev_frame = None
        
        while True:
            frame = self.read_frame()
            if frame is None:
                if scene_start is not None:
                    scenes.append((scene_start, frame.timestamp))
                break
            
            if prev_frame is None:
                prev_frame = frame.frame
                continue
            
            # Calculate frame difference
            diff = np.mean(cv2.absdiff(frame.frame, prev_frame))
            if diff > threshold:
                if scene_start is not None:
                    scenes.append((scene_start, frame.timestamp))
                scene_start = frame.timestamp
            
            prev_frame = frame.frame
        
        return scenes

    def extract_motion(self, frame: VideoFrame) -> np.ndarray:
        """
        Extract motion vectors from frame.

        Args:
            frame: Input video frame.

        Returns:
            np.ndarray: Motion vectors.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame.frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow
        if not hasattr(self, 'prev_gray'):
            self.prev_gray = gray
            return np.zeros_like(frame.frame)
        
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        self.prev_gray = gray
        return flow

    def save_frame(self, frame: VideoFrame, output_path: str) -> None:
        """
        Save frame to file.

        Args:
            frame: Frame to save.
            output_path: Output file path.
        """
        cv2.imwrite(output_path, frame.frame)

    def create_thumbnail(self, timestamp: Optional[float] = None,
                        size: Optional[Tuple[int, int]] = None) -> np.ndarray:
        """
        Create video thumbnail.

        Args:
            timestamp: Optional timestamp for thumbnail frame.
            size: Optional thumbnail size.

        Returns:
            np.ndarray: Thumbnail image.
        """
        if timestamp is not None:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Failed to read frame for thumbnail")
        
        if size is not None:
            frame = cv2.resize(frame, size)
        
        return frame

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cap.release() 