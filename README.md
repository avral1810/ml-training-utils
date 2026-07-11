# ml-training-utils

Small PyTorch training utilities for experiments and lightweight training
loops.

## What is included

- `save_checkpoint`: save model, optimizer, loss, step, epoch, and optional
  metadata to a PyTorch checkpoint file.
- `log_metrics`: write a dictionary of scalar metrics to a TensorBoard-style
  writer.
- `time_execution`: time a function with a decorator or a block with a context
  manager.
- `ConfigObject`, `load_config`, and `config_parser`: load YAML config files
  into nested objects with attribute-style access.

## Installation

For local development:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

For runtime dependencies only:

```bash
python -m pip install -r requirements.txt
```

The runtime dependencies are also declared in `pyproject.toml`, so installing
the package with `pip install .` or `pip install -e .` installs the same runtime
requirements.

## Usage

Save a checkpoint:

```python
import torch.nn as nn
import torch.optim as optim

from ml_training_utils.checkpointing import save_checkpoint

model = nn.Linear(10, 1)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

save_checkpoint(
    model=model,
    optimizer=optimizer,
    train_loss=0.12,
    val_loss=0.18,
    path="checkpoints/latest.pt",
    epoch=3,
    step=500,
    best_metric=0.18,
    config={"lr": 1e-3},
)
```

Log metrics:

```python
from torch.utils.tensorboard import SummaryWriter

from ml_training_utils.logging import log_metrics

writer = SummaryWriter("runs/example")
log_metrics(writer, {"loss": 0.12, "accuracy": 0.94}, step=500, prefix="train")
writer.close()
```

Time code:

```python
from ml_training_utils.timing import time_execution


@time_execution
def train_one_epoch():
    ...


with time_execution("validation"):
    ...
```

Load a YAML config:

```python
from ml_training_utils.config import load_config

config = load_config("configs/train.yaml")

print(config.model.name)
print(config.training.batch_size)
```

Parse a config path from the command line:

```python
from ml_training_utils.config import config_parser

config = config_parser()
```

Then run your script with:

```bash
python train.py --config configs/train.yaml
```

## Development

Run the test suite:

```bash
.venv/bin/python -m pytest
```
