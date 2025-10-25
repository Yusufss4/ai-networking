# Project Migration Guide

## From Original to New Structure

This document explains the migration from the original `shape-detector` project to the new separated structure.

## File Mapping

### Python Files (→ digit-model-ml)

| Original | New Location | Changes |
|----------|--------------|---------|
| `model.py` | `src/digit_model/model.py` | Added type hints, docstrings |
| `data.py` | `src/digit_model/data.py` | Added type hints, docstrings |
| `train.py` | `src/digit_model/train.py` | Added configurable parameters, better logging |
| `eval.py` | `src/digit_model/eval.py` | Added return values, better metrics |
| `predict.py` | `src/digit_model/predict.py` | Refactored into class, added type hints |
| `benchmark.py` | `src/digit_model/benchmark.py` | Improved CLI, added more metrics |
| `requirements.txt` | `pyproject.toml` | Modern Python packaging |
| - | `src/digit_model/cli.py` | **NEW**: CLI entry points |
| - | `src/digit_model/__init__.py` | **NEW**: Package initialization |

### C++ Files (→ digit-detector-cpp)

| Original | New Location | Changes |
|----------|--------------|---------|
| `main.cpp` | `src/main.cpp` | Updated include paths |
| `src/App.h` | `include/digit_detector/App.h` | Better documentation |
| `src/App.cpp` | `src/App.cpp` | Updated include paths |
| `src/InferenceEngine.h` | `include/digit_detector/InferenceEngine.h` | Better documentation |
| `src/InferenceEngine.cpp` | `src/InferenceEngine.cpp` | Updated include paths |
| `src/ImageProcessor.h` | `include/digit_detector/ImageProcessor.h` | Better documentation |
| `src/ImageProcessor.cpp` | `src/ImageProcessor.cpp` | Updated include paths |
| `src/Renderer.h` | `include/digit_detector/Renderer.h` | Better documentation |
| `src/Renderer.cpp` | `src/Renderer.cpp` | Updated include paths |
| `src/types.h` | `include/digit_detector/types.h` | Better documentation |
| `src/nlohmann/json.hpp` | `include/third_party/nlohmann/json.hpp` | Moved to third_party |
| `CMakeLists.txt` | `CMakeLists.txt` | Modern CMake practices, better organization |
| `config.json` | `configs/config.json` | Moved to configs/ directory |

### Configuration Files

| Original | New Location | Changes |
|----------|--------------|---------|
| `config.json` | `digit-detector-cpp/configs/config.json` | Added more options |
| - | `digit-model-ml/configs/default.json` | **NEW**: Python project config |

## Key Improvements

### Python Project (digit-model-ml)

1. **Modern Packaging**
   - `pyproject.toml` instead of `setup.py`
   - Entry points for CLI commands
   - Proper dependency management

2. **Better Organization**
   - `src/` layout for proper packaging
   - Separate tests directory
   - Configuration files in `configs/`

3. **Development Tools**
   - pytest for testing
   - black for formatting
   - ruff for linting
   - mypy for type checking

4. **CLI Commands**
   ```bash
   # Before
   python train.py
   python eval.py
   
   # After
   digit-train
   digit-eval
   digit-predict
   digit-benchmark
   ```

5. **Type Safety**
   - Added type hints throughout
   - Mypy configuration
   - Better IDE support

### C++ Project (digit-detector-cpp)

1. **Directory Structure**
   - Separate `include/` and `src/`
   - Public headers in `include/digit_detector/`
   - Third-party headers in `include/third_party/`

2. **Build System**
   - Modern CMake practices
   - Build script for easy building
   - Makefile for common tasks

3. **Documentation**
   - Comprehensive README
   - Doxygen-style comments
   - Clear architecture documentation

4. **Code Quality**
   - Better const correctness
   - explicit constructors
   - Better documentation

## Migration Steps

### For Users

1. **Clone/Pull the new structure**
   ```bash
   git pull
   ```

2. **Setup Python project**
   ```bash
   cd digit-model-ml
   pip install -e ".[dev]"
   ```

3. **Train model**
   ```bash
   digit-train
   ```

4. **Setup C++ project**
   ```bash
   cd ../digit-detector-cpp
   ./build.sh /path/to/libtorch
   ```

### For Developers

1. **Python development**
   - Install dev dependencies: `pip install -e ".[dev]"`
   - Run tests: `make test`
   - Format code: `make format`
   - Check types: `mypy src/`

2. **C++ development**
   - Build: `make build`
   - Clean: `make clean`
   - Rebuild: `make rebuild`

## Breaking Changes

### Python

1. **Import paths changed**
   ```python
   # Before
   from model import DigitRecognizer
   from data import get_dataloaders
   
   # After
   from digit_model import DigitRecognizer, get_dataloaders
   ```

2. **Script execution changed**
   ```bash
   # Before
   python train.py
   
   # After
   digit-train  # or python -m digit_model.train
   ```

### C++

1. **Include paths changed**
   ```cpp
   // Before
   #include "App.h"
   #include "types.h"
   
   // After (from src/ files)
   #include "App.h"
   #include "types.h"
   // (paths updated in CMakeLists.txt)
   ```

2. **Config file location**
   ```cpp
   // Before
   const std::string config_path = "config.json";
   
   // After
   const std::string config_path = "configs/config.json";
   ```

## Compatibility

### Model Compatibility
- ✅ Models trained with old code work with new code
- ✅ TorchScript exports are compatible
- ✅ Same model architecture

### Data Compatibility
- ✅ Same MNIST dataset
- ✅ Same preprocessing
- ✅ Same normalization constants

## Rollback

If you need to use the original structure:

```bash
cd shape-detector
# Original files are still present
python train.py
python eval.py
```

## Future Improvements

### Planned Enhancements

1. **Python Project**
   - [ ] Add more unit tests
   - [ ] Add integration tests
   - [ ] CI/CD pipeline
   - [ ] Docker support
   - [ ] Model versioning

2. **C++ Project**
   - [ ] Unit tests with Google Test
   - [ ] GPU support
   - [ ] Webcam input support
   - [ ] Performance profiling
   - [ ] Docker support

3. **Documentation**
   - [ ] API documentation with Sphinx (Python)
   - [ ] API documentation with Doxygen (C++)
   - [ ] Tutorials
   - [ ] Video guides

## Questions?

If you have questions about the migration:

1. Check the README files in each project
2. Look at the example configurations
3. Review this migration guide
4. Check the code comments

## Summary

The new structure provides:
- ✅ Better organization
- ✅ Modern tooling
- ✅ Easier development
- ✅ Better documentation
- ✅ Independent versioning
- ✅ Clearer responsibilities

All while maintaining full compatibility with the original functionality!
