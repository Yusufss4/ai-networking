"""Evaluation logic for the digit recognition model."""

from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix

from .data import get_dataloaders
from .model import DigitRecognizer


def evaluate(
    checkpoint_path: str = "models/digit_model.pth",
    batch_size: int = 64,
    device: Optional[str] = None,
) -> dict:
    """
    Evaluate the trained model on the test set.
    
    Args:
        checkpoint_path: Path to the model checkpoint
        batch_size: Batch size for evaluation
        device: Device to evaluate on ('cuda', 'cpu', or None for auto-detect)
        
    Returns:
        Dictionary containing evaluation metrics
    """
    # Setup device
    if device is None:
        device_obj = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device_obj = torch.device(device)
    
    print(f"Evaluating on device: {device_obj}")
    
    # Load data
    _, test_loader = get_dataloaders(batch_size=batch_size)

    # Load model
    model = DigitRecognizer().to(device_obj)
    state = torch.load(checkpoint_path, map_location=device_obj)
    model.load_state_dict(state["model_state"])
    model.eval()

    # Evaluation
    criterion = nn.CrossEntropyLoss()
    test_loss, correct, total = 0.0, 0, 0
    all_preds, all_targets = [], []

    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device_obj), y.to(device_obj)
            logits = model(x)
            loss = criterion(logits, y)
            test_loss += loss.item() * x.size(0)

            preds = torch.argmax(logits, dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(y.cpu().numpy())

    # Calculate metrics
    avg_loss = test_loss / total
    accuracy = correct / total

    print(f"\nTest Loss: {avg_loss:.4f}  |  Accuracy: {accuracy*100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(all_targets, all_preds, digits=4))
    print("Confusion Matrix:")
    print(confusion_matrix(all_targets, all_preds))

    return {
        "loss": avg_loss,
        "accuracy": accuracy,
        "predictions": all_preds,
        "targets": all_targets,
    }


if __name__ == "__main__":
    evaluate()
