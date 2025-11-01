#!/bin/bash
# Complete setup script for both projects

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}AI Networking - Complete Setup${NC}"
echo -e "${GREEN}========================================${NC}"

# Step 1: Setup Python ML Project
echo -e "${GREEN}Step 1: Setting up Python ML project...${NC}"
cd digit-model-ml

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python package..."
pip install -e ".[dev]"

echo -e "${GREEN}Step 2: Training model...${NC}"
digit-train --epochs 5

echo -e "${GREEN}Step 3: Evaluating model...${NC}"
digit-eval

echo -e "${GREEN}Step 4: Copying model to C++ project...${NC}"
cd ..
mkdir -p digit-detector-cpp/models
cp digit-model-ml/models/digit_model.ts digit-detector-cpp/models/

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. To build the C++ detector:"
echo "   cd digit-detector-cpp"
echo "   ./build.sh /path/to/libtorch"
echo ""
echo "2. To run the detector:"
echo "   cd digit-detector-cpp"
echo "   ./build/digit_recognizer"
echo ""
echo -e "${YELLOW}Note: You need to install LibTorch and OpenCV for the C++ project${NC}"
