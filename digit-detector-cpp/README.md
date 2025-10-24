# Digit Detector C++

A real-time digit recognition application using OpenCV and LibTorch (PyTorch C++ API).

## Project Structure

```
digit-detector-cpp/
├── src/                    # Implementation files
│   ├── main.cpp           # Entry point
│   ├── App.cpp            # Main application
│   ├── InferenceEngine.cpp # ML inference engine
│   ├── ImageProcessor.cpp  # Image preprocessing
│   └── Renderer.cpp        # UI rendering
├── include/digit_detector/ # Public headers
│   ├── App.h
│   ├── InferenceEngine.h
│   ├── ImageProcessor.h
│   ├── Renderer.h
│   └── types.h
├── include/third_party/    # Third-party headers (e.g., nlohmann/json)
├── build/                  # Build output directory
├── models/                 # Pre-trained model files (.ts)
├── configs/                # Configuration files
├── CMakeLists.txt          # CMake build configuration
└── README.md               # This file
```

## Features

- **Real-time digit detection** using webcam input
- **High-performance inference** with LibTorch C++ API
- **OpenCV integration** for image processing and UI
- **Modern C++17** codebase with clean architecture
- **Configuration-based** model and parameter management

## Prerequisites

### Required Dependencies

1. **CMake** (>= 3.10)
   ```bash
   sudo apt-get install cmake  # Ubuntu/Debian
   ```

2. **LibTorch** (PyTorch C++ API)
   ```bash
   # Download from https://pytorch.org/get-started/locally/
   # Choose: C++/LibTorch, CPU or CUDA
   wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.0.0%2Bcpu.zip
   unzip libtorch-cxx11-abi-shared-with-deps-2.0.0+cpu.zip
   ```

3. **OpenCV** (>= 4.0)
   ```bash
   sudo apt-get install libopencv-dev  # Ubuntu/Debian
   ```

## Building the Project

### Step 1: Prepare the Model

First, train and export a TorchScript model using the Python ML project:

```bash
cd ../digit-model-ml
pip install -e .
digit-train --epochs 10
```

This will generate `digit_model.ts` in the `models/` directory. Copy it to the C++ project:

```bash
cp models/digit_model.ts ../digit-detector-cpp/models/
```

### Step 2: Configure the Build

```bash
cd digit-detector-cpp
mkdir -p build
cd build

# Configure with CMake (specify LibTorch path)
cmake -DCMAKE_PREFIX_PATH=/path/to/libtorch ..
```

### Step 3: Build

```bash
# Build the project
cmake --build . --config Release

# Or use make directly
make -j$(nproc)
```

### Step 4: Run

```bash
# From the build directory
./digit_recognizer

# Or from the project root
cd ..
./build/digit_recognizer
```

## Configuration

Edit `configs/config.json` to customize:

```json
{
  "model_path": "models/digit_model.ts",
  "confidence_threshold": 0.95
}
```

- `model_path`: Path to the TorchScript model file
- `confidence_threshold`: Minimum confidence for predictions (0.0 - 1.0)

## Usage

### Running the Application

```bash
./build/digit_recognizer
```

### Controls

- **Mouse**: Draw digits in the window
- **Space**: Toggle inference on/off
- **C**: Clear the canvas
- **Q**: Quit the application

### Output

The application displays:
- Live drawing canvas
- Predicted digit (if confidence > threshold)
- Confidence score
- Inference status

## Architecture

### Components

1. **App** (`App.h/cpp`)
   - Main application coordinator
   - Manages component lifecycle
   - Handles the main loop

2. **InferenceEngine** (`InferenceEngine.h/cpp`)
   - Loads and manages the TorchScript model
   - Runs inference on preprocessed tensors
   - Returns predictions with confidence scores

3. **ImageProcessor** (`ImageProcessor.h/cpp`)
   - Converts OpenCV images to PyTorch tensors
   - Applies normalization and preprocessing
   - Handles data type conversions

4. **Renderer** (`Renderer.h/cpp`)
   - Manages OpenCV windows and drawing
   - Renders predictions and UI elements
   - Handles user input events

5. **types.h**
   - Shared data structures (e.g., `Prediction`)
   - Common type definitions

## Development

### Code Style

- **C++ Standard**: C++17
- **Naming Convention**: 
  - Classes: `PascalCase`
  - Methods: `snake_case`
  - Members: `m_prefix_snake_case`
  - Constants: `UPPER_SNAKE_CASE`

### Adding New Features

1. Define interfaces in `include/digit_detector/`
2. Implement in `src/`
3. Update `CMakeLists.txt` if adding new files
4. Rebuild the project

## Troubleshooting

### LibTorch Not Found

```
CMake Error: Could not find Torch
```

**Solution**: Specify the LibTorch path when configuring:
```bash
cmake -DCMAKE_PREFIX_PATH=/absolute/path/to/libtorch ..
```

### OpenCV Not Found

```
CMake Error: Could not find OpenCV
```

**Solution**: Install OpenCV development files:
```bash
sudo apt-get install libopencv-dev
```

### Model Loading Error

```
Error loading model: [model.ts not found]
```

**Solution**: Ensure the model file exists at the path specified in `config.json`

### ABI Compatibility Issues

If you encounter linking errors, ensure:
- LibTorch and your compiler use the same C++ ABI
- Use the correct LibTorch package (cxx11-abi vs pre-cxx11-abi)

## Performance

Expected performance on CPU:
- **Inference**: 2-5ms per image (single thread)
- **Preprocessing**: 1-2ms per frame
- **Total latency**: 3-7ms (~150-300 FPS)

For GPU acceleration:
- Download CUDA-enabled LibTorch
- Modify `config.json` to use CUDA device

## License

MIT License

## Related Projects

- [digit-model-ml](../digit-model-ml/): Python ML training and evaluation
