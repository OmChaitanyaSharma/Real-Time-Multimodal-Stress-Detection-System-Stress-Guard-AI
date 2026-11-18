import base64
import cv2
import numpy as np
from typing import Tuple, Optional

def decode_base64_image(base64_str: str) -> Optional[np.ndarray]:
    """
    Decodes a base64 encoded image string (with or without data URI prefix)
    into a BGR OpenCV NumPy array.
    Guards against decompression bombs and excessive memory allocation.
    """
    try:
        # Enforce maximum base64 string length of 6MB (~4.5MB raw image)
        if len(base64_str) > 6 * 1024 * 1024:
            return None

        if "," in base64_str:
            base64_str = base64_str.split(",", 1)[1]

        image_bytes = base64.b64decode(base64_str)
        # Enforce maximum decoded byte buffer of 5MB
        if len(image_bytes) > 5 * 1024 * 1024:
            return None

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None

        # Defend against dimensional decompression bombs (e.g. 10000x10000 pixel images)
        h, w = img.shape[:2]
        if h > 1920 or w > 1920:
            scale = 1280.0 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        return img
    except Exception as e:
        print(f"Error decoding base64 image: {e}")
        return None

def encode_image_base64(img: np.ndarray, format: str = ".jpg") -> str:
    """
    Encodes an OpenCV image to a base64 string with data URI prefix.
    """
    success, buffer = cv2.imencode(format, img)
    if not success:
        return ""
    b64_str = base64.b64encode(buffer).decode("utf-8")
    mime = "image/jpeg" if format.lower() in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime};base64,{b64_str}"

def calculate_ear(eye_landmarks: np.ndarray) -> float:
    """
    Calculates Eye Aspect Ratio (EAR) given 6 (x, y) landmark coordinates.
    Points ordered as:
    p1: Outer corner
    p2: Upper top-left
    p3: Upper top-right
    p4: Inner corner
    p5: Lower bottom-right
    p6: Lower bottom-left
    """
    if len(eye_landmarks) < 6:
        return 0.30  # Standard relaxed nominal EAR

    p1, p2, p3, p4, p5, p6 = eye_landmarks[:6]
    # Vertical distances
    dist_v1 = np.linalg.norm(p2 - p6)
    dist_v2 = np.linalg.norm(p3 - p5)
    # Horizontal distance
    dist_h = np.linalg.norm(p1 - p4)

    if dist_h == 0:
        return 0.30

    ear = (dist_v1 + dist_v2) / (2.0 * dist_h)
    return float(ear)

def overlay_gradcam(original_bgr: np.ndarray, heatmap: np.ndarray, alpha: float = 0.45) -> np.ndarray:
    """
    Overlays a normalized 2D heatmap (0.0 to 1.0) onto the original image using Jet colormap.
    """
    h, w = original_bgr.shape[:2]
    heatmap_resized = cv2.resize(heatmap, (w, h))
    heatmap_uint8 = np.uint8(255 * np.clip(heatmap_resized, 0, 1))
    color_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    blended = cv2.addWeighted(color_heatmap, alpha, original_bgr, 1 - alpha, 0)
    return blended
