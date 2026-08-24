from dataclasses import dataclass
from typing import Any

@dataclass
class ConfigChange:
    key: str
    old_value: Any
    new_value: Any

@dataclass
class ConfigDiff:
    added: dict[str, Any]
    removed: dict[str, Any]
    changed: list[ConfigChange]

def compare_configs(old: dict[str, Any], new: dict[str, Any]) -> ConfigDiff:
    """比较两个扁平配置字典"""
    old_keys = set(old)
    new_keys = set(new)

    added_keys = new_keys - old_keys
    removed_keys = old_keys - new_keys
    common_keys = old_keys & new_keys

    added = {
        key: new[key]
        for key in sorted(added_keys)
    }

    removed = {
        key: old[key]
        for key in sorted(removed_keys)
    }

    changed = []

    for key in sorted(common_keys):
        if old[key] != new[key]:
            changed.append(
                ConfigChange(
                    key=key,
                    old_value=old[key],
                    new_value=new[key]
                )
            )

    return ConfigDiff(
        added=added,
        removed=removed,
        changed=changed
    )