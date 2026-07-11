import pytest

from ml_training_utils.config import ConfigObject, load_config


def test_config_object_supports_nested_dot_and_item_access():
    config = ConfigObject(
        {
            "model": {
                "name": "tiny-gpt",
                "layers": 4,
            },
            "training": {
                "batch_size": 32,
            },
        }
    )

    assert config.model.name == "tiny-gpt"
    assert config["model"]["layers"] == 4
    assert config.training.batch_size == 32


def test_config_object_wraps_mappings_inside_lists():
    config = ConfigObject(
        {
            "datasets": [
                {"name": "train", "path": "data/train"},
                {"name": "val", "path": "data/val"},
            ]
        }
    )

    assert config.datasets[0].name == "train"
    assert config.datasets[1].path == "data/val"


def test_config_object_as_dict_roundtrip():
    data = {
        "model": {
            "name": "resnet",
        },
        "tags": ["vision", {"split": "train"}],
    }
    config = ConfigObject(data)

    assert config.as_dict() == data


def test_config_object_missing_attribute_raises_attribute_error():
    config = ConfigObject({"model": {"name": "tiny-gpt"}})

    with pytest.raises(AttributeError, match="No config value named 'missing'"):
        _ = config.missing


def test_load_config_reads_yaml_file(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
model:
  name: tiny-gpt
  layers: 4
training:
  batch_size: 32
""".lstrip()
    )

    config = load_config(config_path)

    assert config.model.name == "tiny-gpt"
    assert config.model.layers == 4
    assert config.training.batch_size == 32
