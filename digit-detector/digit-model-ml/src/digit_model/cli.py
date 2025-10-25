"""Command-line interface for the digit model package."""

import argparse
import sys

from . import train as train_module
from . import eval as eval_module
from . import predict as predict_module
from . import benchmark as benchmark_module


def train_cli() -> None:
    """CLI entry point for training."""
    parser = argparse.ArgumentParser(description="Train digit recognition model")
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size")
    parser.add_argument(
        "--out-dir", type=str, default="models", help="Output directory"
    )
    parser.add_argument(
        "--checkpoint-name", type=str, default="digit_model.pth",
        help="Checkpoint filename"
    )
    parser.add_argument(
        "--torchscript-name", type=str, default="digit_model.ts",
        help="TorchScript filename"
    )
    parser.add_argument(
        "--device", type=str, default=None,
        choices=["cpu", "cuda"], help="Device to train on"
    )
    
    args = parser.parse_args()
    
    train_module.train(
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
        out_dir=args.out_dir,
        checkpoint_name=args.checkpoint_name,
        torchscript_name=args.torchscript_name,
        device=args.device,
    )


def eval_cli() -> None:
    """CLI entry point for evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate digit recognition model")
    parser.add_argument(
        "--checkpoint", type=str, default="models/digit_model.pth",
        help="Path to model checkpoint"
    )
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size")
    parser.add_argument(
        "--device", type=str, default=None,
        choices=["cpu", "cuda"], help="Device to evaluate on"
    )
    
    args = parser.parse_args()
    
    eval_module.evaluate(
        checkpoint_path=args.checkpoint,
        batch_size=args.batch_size,
        device=args.device,
    )


def predict_cli() -> None:
    """CLI entry point for prediction."""
    parser = argparse.ArgumentParser(description="Predict digit from image")
    parser.add_argument("image", type=str, help="Path to image file")
    parser.add_argument(
        "--model", type=str, default="models/digit_model.ts",
        help="Path to model file"
    )
    parser.add_argument(
        "--use-checkpoint", action="store_true",
        help="Use PyTorch checkpoint instead of TorchScript"
    )
    
    args = parser.parse_args()
    
    predict_module.predict(
        image_path=args.image,
        model_path=args.model,
        use_torchscript=not args.use_checkpoint,
    )


def benchmark_cli() -> None:
    """CLI entry point for benchmarking."""
    benchmark_module.main()


if __name__ == "__main__":
    print("Use 'digit-train', 'digit-eval', 'digit-predict', or 'digit-benchmark'")
    sys.exit(1)
