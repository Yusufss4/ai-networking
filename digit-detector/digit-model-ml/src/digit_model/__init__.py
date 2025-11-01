"""
Digit Model ML - MNIST Digit Recognition

A PyTorch-based package for training and evaluating MNIST digit recognition models.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .model import DigitRecognizer
from .data import get_dataloaders, MNIST_MEAN, MNIST_STD

__all__ = [
    "DigitRecognizer",
    "get_dataloaders",
    "MNIST_MEAN",
    "MNIST_STD",
]
