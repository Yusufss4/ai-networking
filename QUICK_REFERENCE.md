# Quick Reference Guide

## 📁 Project Structure

```
ai-networking/
├── digit-model-ml/          ← Python ML Project
├── digit-detector-cpp/      ← C++ Detector Project
├── shape-detector/          ← Original (legacy)
├── README.md                ← Main documentation
├── MIGRATION.md             ← Migration guide
├── PROJECT_SUMMARY.md       ← This completion summary
└── setup.sh                 ← Complete setup script
```

## ⚡ Quick Commands

### Python ML Project

```bash
cd digit-model-ml

# Install
pip install -e ".[dev]"

# Train
digit-train --epochs 10

# Evaluate
digit-eval

# Predict single image
digit-predict path/to/image.png

# Benchmark
digit-benchmark --batch 1 --iters 300

# Test
make test

# Format code
make format
```

### C++ Detector Project

```bash
cd digit-detector-cpp

# Build
./build.sh /path/to/libtorch
# or
make build LIBTORCH_PATH=/path/to/libtorch

# Run
./build/digit_recognizer

# Clean
make clean

# Rebuild
make rebuild
```

### Complete Setup (Both Projects)

```bash
# From root directory
./setup.sh
```

## 📝 File Locations

### Python Files

| File Type | Location |
|-----------|----------|
| Source code | `digit-model-ml/src/digit_model/` |
| Tests | `digit-model-ml/tests/` |
| Config | `digit-model-ml/configs/` |
| Models | `digit-model-ml/models/` |
| Data | `digit-model-ml/data/` |

### C++ Files

| File Type | Location |
|-----------|----------|
| Headers | `digit-detector-cpp/include/digit_detector/` |
| Source | `digit-detector-cpp/src/` |
| Config | `digit-detector-cpp/configs/` |
| Models | `digit-detector-cpp/models/` |
| Build | `digit-detector-cpp/build/` |

## 🔧 Common Tasks

### Training a New Model

```bash
cd digit-model-ml
digit-train --epochs 15 --batch-size 128 --lr 0.0005
```

### Evaluating Performance

```bash
cd digit-model-ml
digit-eval --checkpoint models/digit_model.pth
```

### Deploying to C++

```bash
# Copy trained model
cp digit-model-ml/models/digit_model.ts digit-detector-cpp/models/

# Build C++ project
cd digit-detector-cpp
./build.sh /path/to/libtorch

# Run
./build/digit_recognizer
```

### Running Tests

```bash
# Python tests
cd digit-model-ml
pytest tests/ -v

# With coverage
pytest tests/ --cov=digit_model --cov-report=term-missing
```

### Code Quality

```bash
cd digit-model-ml

# Format
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## 🎮 Controls (C++ Detector)

When running the detector:

- **Mouse**: Draw digits
- **C**: Clear canvas
- **Q**: Quit application

## 🐛 Troubleshooting

### Python: Module not found

```bash
# Make sure you installed the package
cd digit-model-ml
pip install -e ".[dev]"
```

### Python: MNIST download fails

```bash
# Download manually or check internet connection
# Data will be in digit-model-ml/data/MNIST/
```

### C++: LibTorch not found

```bash
# Specify LibTorch path
cmake -DCMAKE_PREFIX_PATH=/path/to/libtorch ..
```

### C++: OpenCV not found

```bash
# Install OpenCV
sudo apt-get install libopencv-dev  # Ubuntu/Debian
brew install opencv                  # macOS
```

### C++: Model not found

```bash
# Copy model from Python project
cp ../digit-model-ml/models/digit_model.ts models/

# Or update config.json to point to correct path
```

## 📊 Performance Expectations

### Python Training

- Time: ~2 minutes (10 epochs on CPU)
- Accuracy: >98% on test set
- Model size: ~500KB

### C++ Inference

- Latency: 2-5ms per image
- Throughput: ~200 FPS
- Memory: <50MB

## 🔗 Important Files

### Configuration

- Python: `digit-model-ml/configs/default.json`
- C++: `digit-detector-cpp/configs/config.json`

### Build Files

- Python: `digit-model-ml/pyproject.toml`
- C++: `digit-detector-cpp/CMakeLists.txt`

### Documentation

- Main: `README.md`
- Python: `digit-model-ml/README.md`
- C++: `digit-detector-cpp/README.md`
- Migration: `MIGRATION.md`
- Summary: `PROJECT_SUMMARY.md`

## 💡 Tips

1. **Always activate Python virtual environment** before working on ML project
2. **Retrain model** after changing architecture
3. **Copy TorchScript model** to C++ project after training
4. **Check config files** if paths are wrong
5. **Use absolute paths** for LibTorch in CMake

## 🚀 Next Steps

1. ✅ Train your first model
2. ✅ Test the C++ detector
3. ✅ Experiment with hyperparameters
4. ✅ Try custom images
5. ✅ Read the full documentation

## 📚 Learn More

- [Python Project Details](digit-model-ml/README.md)
- [C++ Project Details](digit-detector-cpp/README.md)
- [Migration Guide](MIGRATION.md)
- [Full Summary](PROJECT_SUMMARY.md)

---

**Happy Coding! 🎉**
