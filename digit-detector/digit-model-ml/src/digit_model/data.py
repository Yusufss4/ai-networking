"""Data loading and preprocessing utilities for MNIST dataset."""

from typing import Tuple

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# MNIST dataset normalization constants
MNIST_MEAN = (0.1307,)
MNIST_STD = (0.3081,)


def get_dataloaders(
    batch_size: int = 64, data_dir: str = "./data", num_workers: int = 2
) -> Tuple[DataLoader, DataLoader]:
    """
    Create training and test data loaders for MNIST dataset.
    
    Args:
        batch_size: Number of samples per batch
        data_dir: Directory to store/load MNIST data
        num_workers: Number of subprocesses for data loading
        
    Returns:
        Tuple of (train_loader, test_loader)
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(MNIST_MEAN, MNIST_STD),
    ])

    train_ds = datasets.MNIST(
        data_dir, train=True, download=True, transform=transform
    )
    test_ds = datasets.MNIST(
        data_dir, train=False, download=True, transform=transform
    )

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )
    
    return train_loader, test_loader
