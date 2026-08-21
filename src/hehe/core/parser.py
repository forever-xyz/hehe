import json
import os
import tomllib
from pathlib import Path
from typing import Any

import yaml
from hehe.core.scanner import get_config_type

def flatten_dict(
        data: dict,
        parent_key: str = "",
) -> dict[str, Any]:
    """
       将嵌套配置扁平化。

       例如：
       {
           "server": {
               "port": 8080
           }
       }

       转换为：
       {
           "server.port": 8080
       }
       """
    result: dict[str, Any] = {}
    for key, value in data.items():
        new_key = f"{parent_key}.{key}" if parent_key else str(key)
        if isinstance(value, dict):
            result.update(flatten_dict(value, new_key))
        else:
            result[new_key] = value

    return result

def parse_config_file(path: Path) -> dict[str, Any]:
    """解析配置文件并返回统一的扁平化结构。"""

    path = path.resolve()

    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")

    config_type = get_config_type(path)

    match config_type:
        case "yaml":
            data = _parse_yaml(path)
        case "yml":
            data = _parse_yaml(path)
        case "json":
            data = _parse_json(path)
        case "toml":
            data = _parse_toml(path)
        case "properties":
            data = _parse_properties(path)
        case "env":
            data = _parse_env(path)
        case _:
            raise ValueError( f"Unsupported config type: {config_type}")

    if not isinstance(data, dict):
        return {}
    return flatten_dict(data)

def _parse_yaml(path: Path) -> dict:
    content = path.read_text(encoding="utf-8-sig")
    data = yaml.safe_load(content)
    return data or {}

def _parse_json(path: Path) -> dict:
    content = path.read_text(encoding="utf-8-sig")
    return json.loads(content)

def _parse_toml(path: Path) -> dict:
    with path.open("rb") as file:
        return tomllib.load(file)

def _parse_properties(path: Path) -> dict:
    result = {}
    content = path.read_text(encoding="utf-8-sig")

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("!"):
            continue

        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            continue
        result[key.strip()] = value.strip()

    return result

def _parse_env(path: Path) -> dict:
    result = {}
    content = path.read_text(encoding="utf-8-sig")

    for line in content.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()

        # 去掉简单字符串引号
        if(len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}):
            value = value[1:-1]
        result[key.key.strip()] = value

    return result