"""Neural network model architecture for digit recognition."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class DigitRecognizer(nn.Module):
    """
    Convolutional Neural Network for MNIST digit recognition.
    
    Architecture:
        - Conv2D (1 -> 32 channels, 3x3 kernel)
        - ReLU + MaxPool2D (2x2)
        - Conv2D (32 -> 64 channels, 3x3 kernel)
        - ReLU + MaxPool2D (2x2)
        - Flatten
        - Linear (64*7*7 -> 128)
        - ReLU
        - Linear (128 -> 10)
    
    Input: (batch, 1, 28, 28) - grayscale images
    Output: (batch, 10) - logits for 10 digit classes
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the network.
        
        Args:
            x: Input tensor of shape (batch, 1, 28, 28)
            
        Returns:
            Output logits of shape (batch, 10)
        """
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
