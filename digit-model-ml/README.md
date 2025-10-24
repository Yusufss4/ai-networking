# Digit Model ML

A PyTorch-based machine learning project for training and evaluating MNIST digit recognition models.

## Project Structure

```
digit-model-ml/
├── src/digit_model/     # Main package source code
│   ├── __init__.py      # Package initialization
│   ├── model.py         # Neural network architecture
│   ├── data.py          # Data loading and preprocessing
│   ├── train.py         # Training logic
│   ├── eval.py          # Evaluation logic
│   ├── predict.py       # Single image prediction
│   ├── benchmark.py     # Performance benchmarking
│   └── cli.py           # Command-line interface
├── tests/               # Unit tests
├── scripts/             # Utility scripts
├── configs/             # Configuration files
├── data/                # Dataset storage (MNIST)
├── models/              # Trained model checkpoints
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # This file
```

## Installation

### Development Installation

```bash
# Clone the repository
cd digit-model-ml

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Production Installation

```bash
pip install .
```

## Usage

### Training a Model

```bash
# Using the CLI
digit-train --epochs 10 --batch-size 64 --lr 0.001

# Or using Python
python -m digit_model.train
```

### Evaluating a Model

```bash
# Using the CLI
digit-eval --checkpoint models/digit_model.pth

# Or using Python
python -m digit_model.eval
```

### Making Predictions

```bash
# Using the CLI
digit-predict path/to/image.png

# Or using Python
python -m digit_model.predict path/to/image.png
```

### Benchmarking

```bash
# Using the CLI
digit-benchmark --batch 1 --iters 300

# Or using Python
python -m digit_model.benchmark
```

## Model Architecture

The model uses a Convolutional Neural Network (CNN) with the following architecture:
- 2 Convolutional layers with ReLU activation
- Max pooling layers
- 2 Fully connected layers
- Input: 28x28 grayscale images
- Output: 10 classes (digits 0-9)

## Model Export

The training script exports two model formats:
1. **PyTorch Checkpoint** (`.pth`): For continued training and evaluation in Python
2. **TorchScript** (`.ts`): For deployment in production (C++ applications)

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
```

### Linting

```bash
ruff check src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Configuration

Configuration files are stored in the `configs/` directory. You can create custom configurations for different training scenarios.

Example configuration:
```json
{
  "epochs": 10,
  "batch_size": 64,
  "learning_rate": 0.001,
  "model_path": "models/digit_model.pth",
  "torchscript_path": "models/digit_model.ts"
}
```

## Output Models

Trained models are saved in the `models/` directory:
- `digit_model.pth`: PyTorch checkpoint
- `digit_model.ts`: TorchScript model for C++ deployment

## Requirements

- Python >= 3.8
- PyTorch >= 2.0.0
- torchvision >= 0.15.0
- NumPy >= 1.21.0
- scikit-learn >= 1.0.0
- Pillow >= 9.0.0

## License

MIT License
