# benchmark.py
import argparse
import statistics
import time

import torch
from PIL import Image
from torchvision import transforms

# The DigitRecognizer class is no longer needed to load the .ts model
from data import MNIST_MEAN, MNIST_STD


def load_model(device: torch.device):
    """Loads the optimized TorchScript model."""
    m = torch.jit.load("digit_model.ts", map_location=device).eval()
    return m


def main():
    p = argparse.ArgumentParser()
    # --ts argument removed
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--iters", type=int, default=300)
    p.add_argument("--warmup", type=int, default=50)
    p.add_argument(
        "--threads", type=int, default=None, help="torch.set_num_threads on CPU"
    )
    p.add_argument(
        "--include_preproc", action="store_true", help="Measure preprocess + model"
    )
    p.add_argument(
        "--image",
        type=str,
        default=None,
        help="Optional image path to include real preprocess",
    )
    args = p.parse_args()

    # Device is hardcoded to CPU
    device = torch.device("cpu")

    # CPU threading control
    if args.threads:
        torch.set_num_threads(args.threads)

    # Model - now loads .ts model directly
    model = load_model(device)
    print("Loaded TorchScript model (digit_model.ts)")

    # Input
    if args.image and args.include_preproc:
        preprocess = transforms.Compose(
            [
                transforms.Grayscale(num_output_channels=1),
                transforms.Resize(
                    (28, 28), interpolation=transforms.InterpolationMode.BILINEAR
                ),
                transforms.ToTensor(),
                transforms.Normalize(MNIST_MEAN, MNIST_STD),
            ]
        )
        img = Image.open(args.image).convert("L")
        x_single = preprocess(img).unsqueeze(0)  # [1,1,28,28]
    else:
        x_single = torch.randn(1, 1, 28, 28)  # synthetic input

    x = x_single.expand(args.batch, -1, -1, -1).contiguous().to(device)

    # Optionally time preprocess as well
    if args.include_preproc and not args.image:
        # Simulate a realistic preprocess cost even with synthetic input
        preprocess = transforms.Normalize(MNIST_MEAN, MNIST_STD)

        def run_once():
            with torch.inference_mode():
                x_local = torch.randn(args.batch, 1, 28, 28)
                x_local = preprocess(x_local)
                # Model dtype is always float32 on CPU
                y = model(x_local.to(device))
                return y

    else:

        def run_once():
            with torch.inference_mode():
                return model(x)

    # Warmup
    for _ in range(args.warmup):
        _ = run_once()

    # Measure
    times = []
    for _ in range(args.iters):
        t0 = time.perf_counter()
        _ = run_once()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0)

    avg = sum(times) / len(times)
    p50 = statistics.median(times)
    p95 = statistics.quantiles(times, n=100)[94] if len(times) >= 100 else max(times)

    fps = 1000.0 / p50 * args.batch  # rough FPS from median latency
    # Updated print statement
    print(
        f"\nDevice: {device.type.upper()}  |  TorchScript: True  |  Batch: {args.batch}"
    )
    if args.threads:
        print(f"CPU threads: {args.threads}")
    print(f"Include preprocess: {args.include_preproc}")
    print(f"Runs: {args.iters} (warmup {args.warmup})")
    print(f"Latency (ms): avg={avg:.3f}  p50={p50:.3f}  p95={p95:.3f}")
    print(f"Throughput ≈ {fps:.1f} FPS")


if __name__ == "__main__":
    main()
