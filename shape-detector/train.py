import torch
import torch.nn as nn
from torch.optim import Adam
from model import DigitRecognizer
from data import get_dataloaders

def train(epochs=2, lr=1e-3, batch_size=64, out_ckpt="digit_model.pth", out_ts="digit_model.ts"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")
    train_loader, _ = get_dataloaders(batch_size=batch_size)

    model = DigitRecognizer().to(device)
    optimizer = Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (x, y) in enumerate(train_loader):
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            if i % 100 == 0:
                print(f"[Epoch {epoch+1}/{epochs}] Step {i:04d}  Loss: {loss.item():.4f}")

        print(f"Epoch {epoch+1} avg loss: {running_loss/len(train_loader):.4f}")

    # Save standard PyTorch checkpoint (best for continued training / evaluation)
    torch.save({"model_state": model.state_dict()}, out_ckpt)
    print(f"Saved checkpoint: {out_ckpt}")

    # Save TorchScript (best for deployment)
    model.eval()
    scripted = torch.jit.script(model.cpu())
    
    # Optimize for CPU inference (for C++ deployment)
    try:
        scripted = torch.jit.optimize_for_inference(scripted)
        print("Applied CPU optimization to TorchScript model")
    except Exception as e:
        print(f"Could not optimize model for inference: {e}")
    
    scripted.save(out_ts)
    print(f"Saved TorchScript: {out_ts}")

if __name__ == "__main__":
    train()
