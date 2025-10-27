# Digit Model ML

A PyTorch-based machine learning project for training and evaluating MNIST digit recognition models.

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

## Model Export

The training script exports two model formats:
1. **PyTorch Checkpoint** (`.pth`): For continued training and evaluation in Python
2. **TorchScript** (`.ts`): For deployment in production (C++ applications)

## Development

### Code Formatting

```bash
black src/
```

### Linting

```bash
ruff check src/
```

### Type Checking

```bash
mypy src/
```
