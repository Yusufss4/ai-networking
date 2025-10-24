# AI Networking - Digit Recognition Project

A modern, well-structured digit recognition system separated into two distinct projects following industry best practices:

- **`digit-model-ml/`** - Python ML project for model training and evaluation
- **`digit-detector-cpp/`** - C++ application for real-time digit detection

## Project Structure

```
ai-networking/
├── digit-model-ml/          # Python ML Training & Evaluation
│   ├── src/digit_model/     # Package source code
│   │   ├── model.py         # Neural network architecture
│   │   ├── data.py          # Data loading utilities
│   │   ├── train.py         # Training logic
│   │   ├── eval.py          # Evaluation logic
│   │   ├── predict.py       # Single image prediction
│   │   ├── benchmark.py     # Performance benchmarking
│   │   └── cli.py           # Command-line interface
│   ├── tests/               # Unit tests
│   ├── configs/             # Configuration files
│   ├── models/              # Trained model checkpoints
│   ├── data/                # Dataset storage
│   ├── pyproject.toml       # Python package configuration
│   └── README.md            # Python project documentation
│
├── digit-detector-cpp/      # C++ Real-time Detector
│   ├── src/                 # Implementation files
│   │   ├── main.cpp         # Entry point
│   │   ├── App.cpp          # Main application
│   │   ├── InferenceEngine.cpp  # ML inference
│   │   ├── ImageProcessor.cpp   # Image preprocessing
│   │   └── Renderer.cpp     # UI rendering
│   ├── include/             # Header files
│   │   ├── digit_detector/  # Public headers
│   │   └── third_party/     # Third-party libraries
│   ├── build/               # Build artifacts (git-ignored)
│   ├── models/              # TorchScript models
│   ├── configs/             # Configuration files
│   ├── CMakeLists.txt       # CMake configuration
│   ├── build.sh             # Build script
│   └── README.md            # C++ project documentation
│
├── shape-detector/          # Original project (legacy)
└── README.md                # This file
```

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

# Install the package
pip install -e ".[dev]"

# Train the model
digit-train --epochs 10

# Evaluate the model
digit-eval

# This generates:
# - models/digit_model.pth (PyTorch checkpoint)
# - models/digit_model.ts (TorchScript for C++)
```

### 2. Run the Detector (C++)

```bash
cd ../digit-detector-cpp

# Copy the trained model
cp ../digit-model-ml/models/digit_model.ts models/

# Build (requires LibTorch and OpenCV)
./build.sh /path/to/libtorch

# Run
./build/digit_recognizer
```

## Detailed Documentation

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
- Comprehensive testing with pytest
- Code quality tools (black, ruff, mypy)
- Dual export: PyTorch checkpoint + TorchScript

**Technology Stack**:
- PyTorch 2.0+
- torchvision
- scikit-learn
- NumPy
- Pillow

### C++ Detector Project (digit-detector-cpp)

**Purpose**: High-performance real-time digit recognition

**Key Features**:
- Modern C++17 codebase
- Clean separation of concerns
- OpenCV for UI and image processing
- LibTorch for inference
- Configuration-based design

**Technology Stack**:
- C++17
- CMake build system
- LibTorch (PyTorch C++ API)
- OpenCV 4.0+
- nlohmann/json

## Workflow

```
┌─────────────────┐
│  MNIST Dataset  │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│  Python ML (digit-model-ml)     │
│  ┌─────────────────────────┐   │
│  │ 1. Train CNN Model      │   │
│  │ 2. Validate on Test Set │   │
│  │ 3. Export to TorchScript│   │
│  └─────────────────────────┘   │
└────────┬────────────────────────┘
         │
         │ digit_model.ts
         v
┌─────────────────────────────────┐
│  C++ Detector (digit-detector)  │
│  ┌─────────────────────────┐   │
│  │ 1. Load TorchScript     │   │
│  │ 2. Capture User Input   │   │
│  │ 3. Preprocess Image     │   │
│  │ 4. Run Inference        │   │
│  │ 5. Display Result       │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

## Why This Structure?

### Separation of Concerns
- **Python**: Best for experimentation, training, and data science workflows
- **C++**: Best for production deployment, performance, and system integration

### Modern Best Practices

#### Python Project
- ✅ `pyproject.toml` for unified configuration
- ✅ `src/` layout for proper packaging
- ✅ Entry points for CLI commands
- ✅ Comprehensive testing
- ✅ Development dependencies separated
- ✅ Type hints and linting

#### C++ Project
- ✅ Separate `include/` and `src/` directories
- ✅ Forward declarations to minimize coupling
- ✅ RAII with smart pointers
- ✅ CMake modern target-based configuration
- ✅ Clear component responsibilities
- ✅ Thread-safe design

### Maintainability
- Each project can be versioned independently
- Clear dependencies and interfaces
- Easy to test each component in isolation
- Documentation close to relevant code

## Development Workflow

### Adding New Features to Python ML

```bash
cd digit-model-ml

# 1. Make changes to src/digit_model/
# 2. Add tests to tests/
# 3. Run tests
make test

# 4. Format code
make format

# 5. Retrain if needed
make train
```

### Modifying C++ Detector

```bash
cd digit-detector-cpp

# 1. Edit headers in include/digit_detector/
# 2. Update implementations in src/
# 3. Rebuild
make rebuild

# 4. Test
make run
```

## Performance

### Python Training
- Training time: ~2 minutes (10 epochs on CPU)
- Test accuracy: >98%
- Model size: ~500KB

### C++ Inference
- Latency: 2-5ms per image (CPU)
- Throughput: ~200 FPS
- Memory: <50MB

## Requirements

### Python Project
- Python >= 3.8
- PyTorch >= 2.0.0
- See `digit-model-ml/pyproject.toml` for full list

### C++ Project
- C++17 compatible compiler
- CMake >= 3.10
- LibTorch (PyTorch C++)
- OpenCV >= 4.0
- See `digit-detector-cpp/README.md` for details

## Contributing

1. Choose the appropriate project (Python ML or C++ Detector)
2. Follow the existing code style
3. Add tests for new features
4. Update documentation

## License

MIT License

## Related Links

- [PyTorch](https://pytorch.org/)
- [LibTorch](https://pytorch.org/cppdocs/)
- [OpenCV](https://opencv.org/)
- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)

## Migration from Original Project

The original `shape-detector/` project has been refactored into:
- `digit-model-ml/` - Contains all Python ML code
- `digit-detector-cpp/` - Contains all C++ detector code

Benefits of the new structure:
- Better organization and maintainability
- Independent versioning and deployment
- Modern tooling and best practices
- Clearer separation of responsibilities
- Easier testing and development
