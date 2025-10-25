"""Unit tests for the model architecture."""

import torch
import pytest

from digit_model.model import DigitRecognizer


def test_model_initialization():
    """Test that model initializes correctly."""
    model = DigitRecognizer()
    assert model is not None


def test_model_forward_pass():
    """Test forward pass with correct input shape."""
    model = DigitRecognizer()
    x = torch.randn(4, 1, 28, 28)  # batch of 4 images
    output = model(x)
    
    assert output.shape == (4, 10), f"Expected shape (4, 10), got {output.shape}"


def test_model_single_image():
    """Test forward pass with single image."""
    model = DigitRecognizer()
    x = torch.randn(1, 1, 28, 28)
    output = model(x)
    
    assert output.shape == (1, 10)


def test_model_output_range():
    """Test that model output is in reasonable range (logits)."""
    model = DigitRecognizer()
    x = torch.randn(2, 1, 28, 28)
    output = model(x)
    
    # Logits should be finite
    assert torch.all(torch.isfinite(output))


def test_model_torchscript_compatible():
    """Test that model can be scripted with TorchScript."""
    model = DigitRecognizer()
    scripted = torch.jit.script(model)
    
    x = torch.randn(1, 1, 28, 28)
    output_original = model(x)
    output_scripted = scripted(x)
    
    assert torch.allclose(output_original, output_scripted, atol=1e-5)
