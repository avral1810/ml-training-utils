from pathlib import Path

import torch
import torch.nn as nn


def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    train_loss: float,
    val_loss: float,
    path: str | Path,
    epoch: int | None = None,
    step: int | None = None,
    best_metric=None,
    config=None,
    extra=None,
):
    if isinstance(path, str):
        path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "train_loss": train_loss,
        "val_loss": val_loss,
        "epoch": epoch,
        "step": step,
    }
    if best_metric is not None:
        data["best_metric"] = best_metric
    if config is not None:
        data["config"] = config
    if extra is not None:
        data["extra"] = extra

    torch.save(data, path)
