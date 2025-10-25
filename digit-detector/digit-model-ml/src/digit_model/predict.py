"""Single image prediction utilities."""

from pathlib import Path
from typing import List, Tuple, Union

import torch
from PIL import Image
from torchvision import transforms

from .data import MNIST_MEAN, MNIST_STD
from .model import DigitRecognizer


class DigitPredictor:
    """
    Predictor class for digit recognition on single images.
    
    Supports both PyTorch checkpoint and TorchScript models.
    """
    
    def __init__(
        self,
        model_path: str,
        use_torchscript: bool = True,
        device: str = "cpu",
    ) -> None:
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to the model file (.pth or .ts)
            use_torchscript: Whether to use TorchScript model
            device: Device to run inference on
        """
        self.device = torch.device(device)
        self.use_torchscript = use_torchscript
        
        # Define preprocessing pipeline
        self.preprocess = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize(
                (28, 28), interpolation=transforms.InterpolationMode.BILINEAR
            ),
            transforms.ToTensor(),
            transforms.Normalize(MNIST_MEAN, MNIST_STD),
        ])
        
        # Load model
        if use_torchscript:
            self.model = torch.jit.load(model_path, map_location=self.device)
        else:
            self.model = DigitRecognizer()
            state = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state["model_state"])
        
        self.model.eval()
    
    def predict(
        self, image_path: Union[str, Path]
    ) -> Tuple[int, List[float]]:
        """
        Predict the digit in an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (predicted_digit, class_probabilities)
        """
        # Load and preprocess image
        img = Image.open(image_path).convert("L")
        x = self.preprocess(img).unsqueeze(0).to(self.device)
        
        # Run inference
        with torch.no_grad():
            logits = self.model(x)
            pred = logits.argmax(dim=1).item()
            probs = logits.softmax(dim=1).squeeze(0).tolist()
        
        return pred, probs


def predict(
    image_path: str,
    model_path: str = "models/digit_model.ts",
    use_torchscript: bool = True,
) -> None:
    """
    Predict and print the digit in an image.
    
    Args:
        image_path: Path to the image file
        model_path: Path to the model file
        use_torchscript: Whether to use TorchScript model
    """
    predictor = DigitPredictor(model_path, use_torchscript)
    pred, probs = predictor.predict(image_path)
    
    print(f"Predicted digit: {pred}")
    print("Class probabilities:", [round(p, 4) for p in probs])


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m digit_model.predict <image_path>")
        sys.exit(1)
    
    predict(sys.argv[1])
