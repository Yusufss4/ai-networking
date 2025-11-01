import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix

from data import get_dataloaders
from model import DigitRecognizer


def evaluate(ckpt_path="digit_model.pth", batch_size=64):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _, test_loader = get_dataloaders(batch_size=batch_size)

    model = DigitRecognizer().to(device)
    state = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(state["model_state"])
    model.eval()

    criterion = nn.CrossEntropyLoss()
    test_loss, correct, total = 0.0, 0, 0
    all_preds, all_targets = [], []

    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = criterion(logits, y)
            test_loss += loss.item() * x.size(0)

            preds = torch.argmax(logits, dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(y.cpu().numpy())

    avg_loss = test_loss / total
    acc = correct / total
    print(f"\nTest Loss: {avg_loss:.4f}  |  Accuracy: {acc*100:.2f}%")

    print("\nClassification Report:")
    print(classification_report(all_targets, all_preds, digits=4))

    print("Confusion Matrix:")
    print(confusion_matrix(all_targets, all_preds))


if __name__ == "__main__":
    evaluate()
