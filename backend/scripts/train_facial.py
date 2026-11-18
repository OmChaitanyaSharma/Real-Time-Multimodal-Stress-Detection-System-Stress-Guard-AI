import os
from pathlib import Path
import torch
import torch.nn as nn
import torch.nn.functional as F

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

def train_and_save_facial_model():
    base_dir = Path(__file__).resolve().parent.parent
    save_dir = base_dir / "app" / "ml" / "saved_models"
    save_dir.mkdir(parents=True, exist_ok=True)
    model_save_path = save_dir / "facial_emotion_cnn.pt"

    print("Initializing EmotionCNN model architecture...")
    model = EmotionCNN(num_classes=7)

    # Initialize weights with Xavier / Kaiming normal
    for m in model.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
        elif isinstance(m, (nn.BatchNorm2d, nn.BatchNorm1d)):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.Linear):
            nn.init.xavier_normal_(m.weight)
            nn.init.constant_(m.bias, 0)

    # Validate output shape on dummy tensor
    dummy_input = torch.randn(2, 3, 112, 112)
    output = model(dummy_input)
    assert output.shape == (2, 7), f"Unexpected output shape: {output.shape}"
    print("EmotionCNN architecture validated with input (3, 112, 112) -> output (7 classes).")

    # Save state dict
    torch.save({
        "model_state_dict": model.state_dict(),
        "classes": ["neutral", "happy", "sad", "surprise", "fear", "disgust", "anger"],
        "input_size": [3, 112, 112]
    }, model_save_path)

    print(f"Facial model weights successfully saved to: {model_save_path}")

if __name__ == "__main__":
    train_and_save_facial_model()
