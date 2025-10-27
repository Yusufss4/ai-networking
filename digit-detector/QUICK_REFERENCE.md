# Quick Reference

## Commands

### Python ML

```bash
cd digit-model-ml
pip install -e ".[dev]"
digit-train --epochs 10
digit-eval
digit-predict path/to/image.png
digit-benchmark --batch 1 --iters 300
```

### C++ Detector

```bash
cd digit-detector-cpp
export LIBTORCH_PATH=/path/to/libtorch
./build.sh
./build/digit_recognizer
```

## Troubleshooting

**Python: Module not found**
```bash
cd digit-model-ml && pip install -e ".[dev]"
```

**C++: LibTorch not found**
```bash
export LIBTORCH_PATH=/path/to/libtorch
./build.sh
```

**C++: OpenCV not found**
```bash
sudo apt-get install libopencv-dev  # Ubuntu/Debian
brew install opencv                  # macOS
```

**C++: Model not found**
```bash
cp ../digit-model-ml/models/digit_model.ts models/
```

## Controls

**C++ Detector:**
- Mouse: Draw digits
- C: Clear canvas  
- Q: Quit

