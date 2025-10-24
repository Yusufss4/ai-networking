#!/bin/bash
# Build script for Digit Detector C++

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Digit Detector Build Script${NC}"
echo -e "${GREEN}========================================${NC}"

# Check for LibTorch
if [ -z "$CMAKE_PREFIX_PATH" ]; then
    echo -e "${YELLOW}Warning: CMAKE_PREFIX_PATH not set${NC}"
    echo "Please set it to your LibTorch installation path:"
    echo "  export CMAKE_PREFIX_PATH=/path/to/libtorch"
    echo ""
    echo "Or pass it as an argument to CMake:"
    echo "  ./build.sh /path/to/libtorch"
    echo ""
fi

# Get LibTorch path from argument if provided
LIBTORCH_PATH=${1:-$CMAKE_PREFIX_PATH}

# Create build directory
mkdir -p build
cd build

# Configure
echo -e "${GREEN}Configuring...${NC}"
if [ -n "$LIBTORCH_PATH" ]; then
    cmake -DCMAKE_PREFIX_PATH="$LIBTORCH_PATH" -DCMAKE_BUILD_TYPE=Release ..
else
    cmake -DCMAKE_BUILD_TYPE=Release ..
fi

# Build
echo -e "${GREEN}Building...${NC}"
cmake --build . --config Release -j$(nproc)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Executable: build/digit_recognizer"
echo ""
echo "To run:"
echo "  cd .."
echo "  ./build/digit_recognizer"
