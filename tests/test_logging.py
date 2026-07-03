from ml_training_utils.logging import log_metrics

class FakeWriter:
    def __init__(self):
        self.scalars = []
    
    def add_scalar(self, tag, value, step):
        self.scalars.append((tag, value, step))

def test_log_metrics_without_prefix():
    writer = FakeWriter()
    log_metrics(
        writer,
        {"loss": 0.1, "accuracy": 0.5},
        step=10,
    )
    assert writer.scalars == [
        ("loss", 0.1, 10),
        ("accuracy", 0.5, 10)

    ]

def test_log_metrics_with_prefix():
    writer = FakeWriter()
    log_metrics(
        writer,
        {"loss": 0.1, "accuracy": 0.5},
        step=10,
        prefix="train",
    )
    assert writer.scalars == [
        ("train/loss", 0.1, 10),
        ("train/accuracy", 0.5, 10)
    ]