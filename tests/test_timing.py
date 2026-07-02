from ml_training_utils.timing import time_execution

def test_time_execution_ctx_manager_prints_label(capsys):
    with time_execution("test123"):
        value = 1 + 1
    captured = capsys.readouterr()
    assert value == 2
    assert "test123" in captured.out
    assert 'completed in' in captured.out

def test_time_execution_decorator(capsys):
    @time_execution
    def add(a: int, b: int) -> int:
        return a + b
    
    result = add(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    assert "add" in captured.out
    assert 'completed in' in captured.out

def test_time_execution_context_manager_runs_block(capsys):
    values = []

    with time_execution("append_block"):
        values.append("ran")

    assert values == ["ran"]