"""Performance benchmarking utilities for the model."""

import argparse
import statistics
import time
from typing import Optional

import torch
from PIL import Image
from torchvision import transforms

from .data import MNIST_MEAN, MNIST_STD


def load_model(model_path: str, device: torch.device) -> torch.jit.ScriptModule:
    """
    Load a TorchScript model.
    
    Args:
        model_path: Path to the TorchScript model file
        device: Device to load the model on
        
    Returns:
        Loaded TorchScript model
    """
    model = torch.jit.load(model_path, map_location=device)
    model.eval()
    return model


def benchmark(
    model_path: str = "models/digit_model.ts",
    batch_size: int = 1,
    iterations: int = 300,
    warmup: int = 50,
    num_threads: Optional[int] = None,
    include_preprocess: bool = False,
    image_path: Optional[str] = None,
    device: str = "cpu",
) -> dict:
    """
    Benchmark model inference performance.
    
    Args:
        model_path: Path to the TorchScript model
        batch_size: Batch size for inference
        iterations: Number of iterations to benchmark
        warmup: Number of warmup iterations
        num_threads: Number of CPU threads (None for default)
        include_preprocess: Whether to include preprocessing in timing
        image_path: Optional real image path for preprocessing
        device: Device to run on ('cpu' or 'cuda')
        
    Returns:
        Dictionary containing benchmark statistics
    """
    # Setup device
    device_obj = torch.device(device)
    
    # CPU threading control
    if num_threads is not None and device == "cpu":
        torch.set_num_threads(num_threads)
    
    # Load model
    model = load_model(model_path, device_obj)
    print(f"Loaded TorchScript model from {model_path}")
    
    # Prepare input
    if image_path and include_preprocess:
        preprocess = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize(
                (28, 28), interpolation=transforms.InterpolationMode.BILINEAR
            ),
            transforms.ToTensor(),
            transforms.Normalize(MNIST_MEAN, MNIST_STD),
        ])
        img = Image.open(image_path).convert("L")
        x_single = preprocess(img).unsqueeze(0)
    else:
        x_single = torch.randn(1, 1, 28, 28)
    
    x = x_single.expand(batch_size, -1, -1, -1).contiguous().to(device_obj)
    
    # Define inference function
    if include_preprocess and not image_path:
        preprocess_norm = transforms.Normalize(MNIST_MEAN, MNIST_STD)
        
        def run_once():
            with torch.inference_mode():
                x_local = torch.randn(batch_size, 1, 28, 28)
                x_local = preprocess_norm(x_local)
                return model(x_local.to(device_obj))
    else:
        def run_once():
            with torch.inference_mode():
                return model(x)
    
    # Warmup
    for _ in range(warmup):
        _ = run_once()
    
    # Benchmark
    times = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        _ = run_once()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0)  # Convert to milliseconds
    
    # Calculate statistics
    avg = sum(times) / len(times)
    p50 = statistics.median(times)
    p95 = statistics.quantiles(times, n=100)[94] if len(times) >= 100 else max(times)
    fps = 1000.0 / p50 * batch_size
    
    # Print results
    print(f"\nDevice: {device.upper()}  |  Batch: {batch_size}")
    if num_threads:
        print(f"CPU threads: {num_threads}")
    print(f"Include preprocess: {include_preprocess}")
    print(f"Runs: {iterations} (warmup {warmup})")
    print(f"Latency (ms): avg={avg:.3f}  p50={p50:.3f}  p95={p95:.3f}")
    print(f"Throughput ≈ {fps:.1f} FPS")
    
    return {
        "avg_latency_ms": avg,
        "p50_latency_ms": p50,
        "p95_latency_ms": p95,
        "fps": fps,
        "batch_size": batch_size,
        "device": device,
    }


def main() -> None:
    """Command-line interface for benchmarking."""
    parser = argparse.ArgumentParser(description="Benchmark digit recognition model")
    parser.add_argument(
        "--model", type=str, default="models/digit_model.ts",
        help="Path to TorchScript model"
    )
    parser.add_argument("--batch", type=int, default=1, help="Batch size")
    parser.add_argument("--iters", type=int, default=300, help="Number of iterations")
    parser.add_argument("--warmup", type=int, default=50, help="Warmup iterations")
    parser.add_argument(
        "--threads", type=int, default=None, help="CPU threads"
    )
    parser.add_argument(
        "--include_preproc", action="store_true",
        help="Include preprocessing in timing"
    )
    parser.add_argument(
        "--image", type=str, default=None,
        help="Optional image path for preprocessing"
    )
    parser.add_argument(
        "--device", type=str, default="cpu",
        choices=["cpu", "cuda"], help="Device to run on"
    )
    
    args = parser.parse_args()
    
    benchmark(
        model_path=args.model,
        batch_size=args.batch,
        iterations=args.iters,
        warmup=args.warmup,
        num_threads=args.threads,
        include_preprocess=args.include_preproc,
        image_path=args.image,
        device=args.device,
    )


if __name__ == "__main__":
    main()
