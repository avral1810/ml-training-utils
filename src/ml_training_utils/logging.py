from typing import Mapping

def log_metrics(
    writer,
    metrics: Mapping[str, float],
    step: int, 
    prefix: str | None=None,
):
    for name, value in metrics.items():
        if prefix is None:
            tag = name
        else:
            tag = f"{prefix}/{name}"
        writer.add_scalar(tag, value, step)
