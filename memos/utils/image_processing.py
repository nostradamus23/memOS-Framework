"""
Image processing utilities for MemOS AI Framework.
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Union, Tuple, Optional

def load_image(image_path: Union[str, Path]) -> np.ndarray:
    """
    Load an image from file.

    Args:
        image_path: Path to the image file.

    Returns:
        np.ndarray: Image data as numpy array.
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Read image using OpenCV
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Convert from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def preprocess_image(image: np.ndarray, 
                    target_size: Optional[Tuple[int, int]] = None,
                    normalize: bool = True) -> np.ndarray:
    """
    Preprocess an image for model input.

    Args:
        image: Input image as numpy array.
        target_size: Optional target size (height, width).
        normalize: Whether to normalize pixel values.

    Returns:
        np.ndarray: Preprocessed image.
    """
    # Resize if target size is specified
    if target_size is not None:
        image = cv2.resize(image, target_size[::-1])  # OpenCV uses (width, height)
    
    # Convert to float32
    image = image.astype(np.float32)
    
    # Normalize if requested
    if normalize:
        image = image / 255.0
    
    return image

def extract_features(image: np.ndarray) -> dict:
    """
    Extract basic image features.

    Args:
        image: Input image as numpy array.

    Returns:
        dict: Dictionary of extracted features.
    """
    features = {}
    
    # Basic image properties
    features["height"], features["width"], features["channels"] = image.shape
    
    # Color statistics
    features["mean_color"] = image.mean(axis=(0, 1)).tolist()
    features["std_color"] = image.std(axis=(0, 1)).tolist()
    
    # Convert to grayscale for additional features
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Edge detection
    edges = cv2.Canny(gray, 100, 200)
    features["edge_density"] = edges.mean() / 255.0
    
    # Basic texture features using GLCM
    features["contrast"] = cv2.convertScaleAbs(gray).std()
    
    return features

def save_image(image: np.ndarray, 
              output_path: Union[str, Path], 
              format: str = "PNG") -> None:
    """
    Save an image to file.

    Args:
        image: Image data as numpy array.
        output_path: Path to save the image.
        format: Image format (e.g., "PNG", "JPEG").
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to PIL Image
    if image.dtype == np.float32 or image.dtype == np.float64:
        image = (image * 255).astype(np.uint8)
    pil_image = Image.fromarray(image)
    
    # Save image
    pil_image.save(str(output_path), format=format)

def apply_transformations(image: np.ndarray,
                        rotate: Optional[float] = None,
                        flip: Optional[bool] = None,
                        brightness: Optional[float] = None,
                        contrast: Optional[float] = None) -> np.ndarray:
    """
    Apply various transformations to an image.

    Args:
        image: Input image as numpy array.
        rotate: Optional rotation angle in degrees.
        flip: Optional boolean for horizontal flip.
        brightness: Optional brightness adjustment factor.
        contrast: Optional contrast adjustment factor.

    Returns:
        np.ndarray: Transformed image.
    """
    result = image.copy()
    
    # Rotate
    if rotate is not None:
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, rotate, 1.0)
        result = cv2.warpAffine(result, rotation_matrix, (width, height))
    
    # Flip
    if flip:
        result = cv2.flip(result, 1)  # 1 for horizontal flip
    
    # Adjust brightness
    if brightness is not None:
        result = cv2.convertScaleAbs(result, alpha=brightness, beta=0)
    
    # Adjust contrast
    if contrast is not None:
        result = cv2.convertScaleAbs(result, alpha=contrast, beta=0)
    
    return result 