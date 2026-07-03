import torch
import torch.nn as nn

from ml_training_utils.checkpointing import save_checkpoint


def test_save_checkpoint_writes_training_state(tmp_path):
    model = nn.Linear(2, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    checkpoint_path = tmp_path / "checkpoints" / "step-1.pt"

    save_checkpoint(
        model=model,
        optimizer=optimizer,
        train_loss=0.5,
        val_loss=0.75,
        path=checkpoint_path,
        epoch=2,
        step=10,
        best_metric=0.75,
        config={"lr": 0.1},
        extra={"split": "validation"},
    )

    checkpoint = torch.load(checkpoint_path, weights_only=False)

    assert checkpoint["model_state_dict"].keys() == model.state_dict().keys()
    assert checkpoint["optimizer_state_dict"].keys() == optimizer.state_dict().keys()
    assert checkpoint["train_loss"] == 0.5
    assert checkpoint["val_loss"] == 0.75
    assert checkpoint["epoch"] == 2
    assert checkpoint["step"] == 10
    assert checkpoint["best_metric"] == 0.75
    assert checkpoint["config"] == {"lr": 0.1}
    assert checkpoint["extra"] == {"split": "validation"}
