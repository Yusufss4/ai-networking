# AI Networking - Digit Recognition Project

A modern, well-structured digit recognition system separated into two distinct projects following industry best practices:

- **`digit-model-ml/`** - Python ML project for model training and evaluation
- **`digit-detector-cpp/`** - C++ application for real-time digit detection

## Overview

This project demonstrates a complete ML workflow from training to deployment:

1. **Training** (Python) - Train a CNN on MNIST dataset
2. **Evaluation** (Python) - Validate model performance
3. **Export** (Python) - Convert to TorchScript for deployment
4. **Deployment** (C++) - Real-time inference with OpenCV

## Quick Start

### 1. Train the Model (Python)

```bash
cd digit-model-ml
pip install -e ".[dev]"
digit-train --epochs 10
digit-eval
digit-predict path/to/image.png
digit-benchmark --batch 1 --iters 300
```

### 2. Run the Detector (C++)

```bash
cd digit-detector-cpp
cp ../digit-model-ml/models/digit_model.ts models/
export LIBTORCH_PATH=/path/to/libtorch
./build.sh
./build/digit_recognizer
```

## Documentation

### Python ML Project

See [digit-model-ml/README.md](digit-model-ml/README.md) for:
- Installation instructions
- Training configuration
- Evaluation metrics
- Benchmarking
- API reference

### C++ Detector Project

See [digit-detector-cpp/README.md](digit-detector-cpp/README.md) for:
- Build instructions
- Dependencies setup
- Architecture overview
- Usage guide
- Troubleshooting

## Architecture

### Python ML Project (digit-model-ml)

**Purpose**: Model development, training, and evaluation

**Key Features**:
- Modern Python packaging with `pyproject.toml`
- CLI tools for training, evaluation, and prediction
- Code quality tools (black, ruff, mypy)
- Dual export: PyTorch checkpoint + TorchScript

**Technology Stack**:
- PyTorch 2.0+, torchvision, scikit-learn, NumPy

**C++ Detector** - High-performance real-time digit recognition
- C++17, CMake, LibTorch, OpenCV 4.0+

See project-specific READMEs for detailed setup and usage instructions.

## License

MIT License

## Related Links

- [PyTorch](https://pytorch.org/)
- [LibTorch](https://pytorch.org/cppdocs/)
- [OpenCV](https://opencv.org/)
- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)