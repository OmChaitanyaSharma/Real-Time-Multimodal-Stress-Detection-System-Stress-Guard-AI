import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from app.utils.helpers import decode_base64_image, encode_image_base64, calculate_ear, overlay_gradcam

class EmotionCNN(nn.Module):
    """
    Lightweight, highly optimized deep CNN for real-time facial expression classification.
    Designed for rapid CPU inference (<30ms) on standard laptop hardware.
    Outputs probabilities for 7 standard emotions:
    [0: neutral, 1: happy, 2: sad, 3: surprise, 4: fear, 5: disgust, 6: anger]
    """
    def __init__(self, num_classes: int = 7):
        super(EmotionCNN, self).__init__()
        
        # Block 1
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.drop1 = nn.Dropout2d(0.2)

        # Block 2
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.drop2 = nn.Dropout2d(0.25)

        # Block 3 (Target layer for Grad-CAM)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(256)
        self.pool3 = nn.MaxPool2d(2, 2)
        self.drop3 = nn.Dropout2d(0.3)

        # Global average pooling & Classifier
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(256, 128)
        self.bn_fc = nn.BatchNorm1d(128)
        self.drop4 = nn.Dropout(0.4)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.pool1(F.relu(self.bn2(self.conv2(x))))
        x = self.drop1(x)

        x = self.pool2(F.relu(self.bn3(self.conv3(x))))
        x = self.drop2(x)

        x = self.pool3(F.relu(self.bn4(self.conv4(x))))
        x = self.drop3(x)

        x = self.global_pool(x)
        x = torch.flatten(x, 1)
        x = F.relu(self.bn_fc(self.fc1(x)))
        x = self.drop4(x)
        logits = self.fc2(x)
        return logits

class GradCAM:
    """
    Computes Gradient-weighted Class Activation Mapping (Grad-CAM)
    on the final convolutional layer of EmotionCNN.
    """
    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self._forward_hook)
        self.target_layer.register_full_backward_hook(self._backward_hook)

    def _forward_hook(self, module, input, output):
        self.activations = output

    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate(self, input_tensor: torch.Tensor, class_idx: int) -> np.ndarray:
        self.model.zero_grad()
        output = self.model(input_tensor)
        target_score = output[0, class_idx]
        target_score.backward(retain_graph=True)

        # Pool gradients across spatial dimensions (GAP)
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        activations = self.activations[0]

        # Weight activations by gradients
        for i in range(activations.size(0)):
            activations[i, :, :] *= pooled_gradients[i]

        heatmap = torch.mean(activations, dim=0).squeeze().detach().cpu().numpy()
        heatmap = np.maximum(heatmap, 0) # ReLU
        if np.max(heatmap) > 0:
            heatmap = heatmap / np.max(heatmap)
        else:
            heatmap = np.zeros_like(heatmap)
        return heatmap

class FacialAnalysisEngine:
    def __init__(self):
        self.classes = ["neutral", "happy", "sad", "surprise", "fear", "disgust", "anger"]
        self.device = torch.device("cpu")
        self.model = EmotionCNN(num_classes=len(self.classes)).to(self.device)
        self.model.eval()

        self.models_dir = Path(__file__).resolve().parent / "saved_models"
        self.weights_path = self.models_dir / "facial_emotion_cnn.pt"

        if self.weights_path.exists():
            try:
                checkpoint = torch.load(self.weights_path, map_location=self.device)
                self.model.load_state_dict(checkpoint["model_state_dict"])
                print("Loaded trained EmotionCNN weights.")
            except Exception as e:
                print(f"Could not load saved weights: {e}, using initialized weights.")
        else:
            print("EmotionCNN weights not found on disk, running initialized model.")

        # Setup GradCAM on conv4 (the deepest 256-channel conv block)
        self.gradcam = GradCAM(self.model, self.model.conv4)

        # Load Haar cascade for face and eye detection from local cascades directory
        cascades_dir = Path(__file__).resolve().parent / "cascades"
        face_xml = str(cascades_dir / "haarcascade_frontalface_default.xml")
        eye_xml = str(cascades_dir / "haarcascade_eye.xml")

        self.face_cascade = cv2.CascadeClassifier(face_xml)
        self.eye_cascade = cv2.CascadeClassifier(eye_xml)

    def analyze_frame(
        self,
        base64_str: str,
        client_ear: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Processes an incoming base64 webcam frame:
        1. Detects face ROI.
        2. Estimates Eye Aspect Ratio (EAR) from ocular regions or accepts client EAR.
        3. Classifies facial expression into 7 emotions.
        4. Calculates visual stress score based on negative valence / high arousal.
        5. Computes Grad-CAM visual attention heatmap.
        """
        img = decode_base64_image(base64_str)
        if img is None:
            return {
                "face_detected": False,
                "dominant_emotion": "neutral",
                "emotion_probabilities": {c: round(1.0 / len(self.classes), 3) for c in self.classes},
                "eye_aspect_ratio": 0.28,
                "facial_stress_score": 0.20,
                "gradcam_base64": None,
                "confidence": 0.0,
                "message": "Invalid or unreadable image frame"
            }

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

        if len(faces) == 0:
            # Fallback: analyze central crop if face detector missed due to lighting
            h, w = img.shape[:2]
            cx, cy = w // 2, h // 2
            side = min(w, h) // 2
            x, y, w_face, h_face = max(0, cx - side//2), max(0, cy - side//2), side, side
            face_detected = False
        else:
            # Take the largest detected face
            x, y, w_face, h_face = max(faces, key=lambda f: f[2] * f[3])
            face_detected = True

        face_roi = img[y:y+h_face, x:x+w_face]

        # Calculate Eye Aspect Ratio (EAR)
        if client_ear is not None and 0.05 < client_ear < 0.60:
            ear = float(client_ear)
        else:
            # Estimate EAR from Haar eye detections in upper face half
            face_gray = gray[y:y+h_face, x:x+w_face]
            upper_gray = face_gray[:int(h_face * 0.6), :]
            eyes = self.eye_cascade.detectMultiScale(upper_gray, scaleFactor=1.1, minNeighbors=4, minSize=(15, 15))
            if len(eyes) >= 2:
                # Average aspect ratio (height / width) of detected eye bounding boxes
                eye_ratios = [float(eh) / float(ew) for (ex, ey, ew, eh) in eyes[:2]]
                ear = float(np.mean(eye_ratios) * 0.55) # Scale to standard EAR range
            else:
                ear = 0.28 # Default open eye nominal value

        # Prepare tensor for CNN inference (112x112 RGB normalized)
        face_resized = cv2.resize(face_roi, (112, 112))
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        tensor = torch.from_numpy(face_rgb).float().permute(2, 0, 1) / 255.0
        # Standard ImageNet normalization
        mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
        tensor = (tensor - mean) / std
        input_tensor = tensor.unsqueeze(0).to(self.device)

        # Model Inference
        with torch.enable_grad():
            input_tensor.requires_grad = True
            logits = self.model(input_tensor)
            probs = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
            winner_idx = int(np.argmax(probs))

            # Grad-CAM extraction
            try:
                heatmap = self.gradcam.generate(input_tensor, winner_idx)
                overlay = overlay_gradcam(face_roi, heatmap, alpha=0.45)
                gradcam_base64 = encode_image_base64(overlay)
            except Exception as e:
                print(f"Grad-CAM computation warning: {e}")
                gradcam_base64 = encode_image_base64(face_roi)

        emotion_distribution = {
            cls_name: round(float(probs[i]), 4)
            for i, cls_name in enumerate(self.classes)
        }
        dominant_emotion = self.classes[winner_idx]

        # Calculate academic facial stress score:
        # Negative valence / high arousal emotions + ocular fatigue (low EAR)
        anger = emotion_distribution["anger"]
        fear = emotion_distribution["fear"]
        sad = emotion_distribution["sad"]
        disgust = emotion_distribution["disgust"]
        surprise = emotion_distribution["surprise"]
        neutral = emotion_distribution["neutral"]
        happy = emotion_distribution["happy"]

        emotion_stress = (
            (anger * 0.95) +
            (fear * 0.90) +
            (sad * 0.70) +
            (disgust * 0.75) +
            (surprise * 0.30) +
            (neutral * 0.15) +
            (happy * 0.02)
        )

        ear_strain = 0.0
        if ear < 0.22:
            ear_strain = min(0.35, (0.22 - ear) * 2.5)
        elif ear > 0.38:
            ear_strain = min(0.20, (ear - 0.38) * 1.5)

        facial_stress_score = float(np.clip((0.75 * emotion_stress) + (0.25 * ear_strain), 0.0, 1.0))
        confidence = float(np.clip(probs[winner_idx] + (0.20 if face_detected else -0.10), 0.50, 0.98))

        return {
            "face_detected": face_detected,
            "dominant_emotion": dominant_emotion,
            "emotion_probabilities": emotion_distribution,
            "eye_aspect_ratio": round(ear, 3),
            "facial_stress_score": round(facial_stress_score, 4),
            "gradcam_base64": gradcam_base64,
            "confidence": round(confidence, 3),
            "message": "Face analyzed successfully" if face_detected else "Face approximated (low contrast / occlusion)"
        }

facial_engine = FacialAnalysisEngine()
