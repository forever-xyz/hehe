from dataclasses import dataclass
from typing import Any

@dataclass
class ConfigCheckResult:
    missing_in_first: dict[str, Any]
    missing_in_second: dict[str, Any]
    shared_count: int

def check_configs(
        first: dict[str, Any],
        second: dict[str, Any]
) -> ConfigCheckResult:
    """检查两个配置是否拥有相同的配置项。"""
    first_keys = set(first)
    second_keys = set(second)

    missing_in_first_keys = second_keys - first_keys
    missing_in_second_keys = first_keys - second_keys

    shared_keys = first_keys & second_keys

    missing_in_first = {
        key: second[key]
        for key in sorted(missing_in_first_keys)
    }

    missing_in_second = {
        key: first[key]
        for key in sorted(missing_in_second_keys)
    }

    return ConfigCheckResult(
        missing_in_first=missing_in_first,
        missing_in_second=missing_in_second,
        shared_count=len(shared_keys)
    )