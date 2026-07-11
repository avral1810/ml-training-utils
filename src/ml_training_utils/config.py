import argparse
import yaml
from collections.abc import Mapping
from typing import Any

class ConfigObject:
    def __init__(self, data: Mapping[str, Any]):
        object.__setattr__(self, "_data", {})
        for key, value in data.items():
            self._data[key] = self._wrap(value)
    
    @classmethod
    def _wrap(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            return cls(value)
        if isinstance(value, list):
            return [cls._wrap(item) for item in value]
        return value
    
    @classmethod
    def _unwrap(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return {
                key: cls._unwrap(item)
                for key, item in value._data.items()
            }
        if isinstance(value, list):
            return [cls._unwrap(item) for item in value]
        return value
        

    def __getattr__(self, key: str) -> Any:
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(f"No config value named {key!r}") from None
    
    def __getitem__(self, key: str) -> Any:
        return self._data[key]
    
    def __setattr__(self, key: str, value: Any) -> None:
        self._data[key] = self._wrap(value)
    
    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = self._wrap(value)

    def as_dict(self) -> dict[str, Any]:
        return self._unwrap(self)
    
    def __repr__(self) -> str:
        return repr(self._unwrap(self))
    
        
def config_parser():
    parser = argparse.ArgumentParser(description="Write model name from Hugging face")
    parser.add_argument(
        "-c",
        "--config",
        default="config/",
        help="Config File Name",
    )
    args = parser.parse_args()
    print(args.config)
    with open(args.config, 'r') as f:
        return ConfigObject(yaml.safe_load(f))
