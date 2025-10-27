# Digit Detector C++

A real-time digit recognition application using OpenCV and LibTorch (PyTorch C++ API).

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