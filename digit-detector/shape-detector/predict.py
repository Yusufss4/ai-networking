import torch
from PIL import Image
from torchvision import transforms

from data import MNIST_MEAN, MNIST_STD
from model import DigitRecognizer

# Inference with TorchScript or with the Python class; choose one:

USE_TORCHSCRIPT = True
TS_PATH = "digit_model.ts"
CKPT_PATH = "digit_model.pth"

preprocess = transforms.Compose(
    [
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize(
            (28, 28), interpolation=transforms.InterpolationMode.BILINEAR
        ),
        transforms.ToTensor(),
        transforms.Normalize(MNIST_MEAN, MNIST_STD),
    ]
)


def predict(image_path: str):
    img = Image.open(image_path).convert("L")
    x = preprocess(img).unsqueeze(0)  # [1,1,28,28]

    if USE_TORCHSCRIPT:
        model = torch.jit.load(TS_PATH).eval()
    else:
        model = DigitRecognizer()
        state = torch.load(CKPT_PATH, map_location="cpu")
        model.load_state_dict(state["model_state"])
        model.eval()

    with torch.no_grad():
        logits = model(x)
        pred = logits.argmax(dim=1).item()
        probs = logits.softmax(dim=1).squeeze(0).tolist()

    print(f"Predicted digit: {pred}")
    print("Class probabilities:", [round(p, 4) for p in probs])


if __name__ == "__main__":
    # Example: python predict.py path/to/my_digit.png
    import sys

    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        raise SystemExit(1)
    predict(sys.argv[1])
