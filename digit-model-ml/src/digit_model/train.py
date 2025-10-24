"""Training logic for the digit recognition model."""

from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from torch.optim import Adam

from .data import get_dataloaders
from .model import DigitRecognizer


def train(
    epochs: int = 10,
    lr: float = 1e-3,
    batch_size: int = 64,
    out_dir: str = "models",
    checkpoint_name: str = "digit_model.pth",
    torchscript_name: str = "digit_model.ts",
    device: Optional[str] = None,
) -> None:
    """
    Train the digit recognition model.
    
    Args:
        epochs: Number of training epochs
        lr: Learning rate
        batch_size: Batch size for training
        out_dir: Output directory for saved models
        checkpoint_name: Name for the PyTorch checkpoint file
        torchscript_name: Name for the TorchScript export file
        device: Device to train on ('cuda', 'cpu', or None for auto-detect)
    """
    # Setup device
    if device is None:
        device_obj = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device_obj = torch.device(device)
    
    print(f"Training on device: {device_obj}")
    
    # Create output directory
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Load data
    train_loader, _ = get_dataloaders(batch_size=batch_size)

    # Initialize model, optimizer, and loss
    model = DigitRecognizer().to(device_obj)
    optimizer = Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    # Training loop
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (x, y) in enumerate(train_loader):
            x, y = x.to(device_obj), y.to(device_obj)
            
            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()

            if i % 100 == 0:
                print(
                    f"[Epoch {epoch+1}/{epochs}] Step {i:04d}  Loss: {loss.item():.4f}"
                )

        avg_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1} avg loss: {avg_loss:.4f}")

    # Save PyTorch checkpoint
    checkpoint_path = out_path / checkpoint_name
    torch.save({"model_state": model.state_dict()}, checkpoint_path)
    print(f"Saved checkpoint: {checkpoint_path}")

    # Save TorchScript model
    model.eval()
    scripted = torch.jit.script(model.cpu())
    torchscript_path = out_path / torchscript_name
    scripted.save(str(torchscript_path))
    print(f"Saved TorchScript: {torchscript_path}")


if __name__ == "__main__":
    train()
