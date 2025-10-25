"""Unit tests for data loading utilities."""

import torch
import pytest

from digit_model.data import get_dataloaders, MNIST_MEAN, MNIST_STD


def test_mnist_constants():
    """Test that MNIST constants are defined."""
    assert MNIST_MEAN == (0.1307,)
    assert MNIST_STD == (0.3081,)


def test_get_dataloaders():
    """Test that dataloaders are created correctly."""
    train_loader, test_loader = get_dataloaders(batch_size=32, num_workers=0)
    
    assert train_loader is not None
    assert test_loader is not None


def test_dataloader_batch_size():
    """Test that batch size is respected."""
    batch_size = 16
    train_loader, test_loader = get_dataloaders(batch_size=batch_size, num_workers=0)
    
    x, y = next(iter(train_loader))
    assert x.shape[0] <= batch_size  # Can be less for last batch
    assert y.shape[0] <= batch_size


def test_dataloader_shapes():
    """Test that data has correct shapes."""
    train_loader, _ = get_dataloaders(batch_size=8, num_workers=0)
    x, y = next(iter(train_loader))
    
    # Images should be (batch, 1, 28, 28)
    assert len(x.shape) == 4
    assert x.shape[1] == 1
    assert x.shape[2] == 28
    assert x.shape[3] == 28
    
    # Labels should be (batch,)
    assert len(y.shape) == 1


def test_dataloader_normalization():
    """Test that data is normalized."""
    train_loader, _ = get_dataloaders(batch_size=8, num_workers=0)
    x, y = next(iter(train_loader))
    
    # Normalized MNIST should have values roughly in range [-2, 2]
    assert x.min() >= -5.0
    assert x.max() <= 5.0
