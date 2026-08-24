from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hehe.core.parser import parse_config_file
from hehe.core.scanner import scan_config_files

@dataclass
class SearchMatch:
    file: Path
    key: str
    value: Any

def search_configs(
        root: Path,
        keyword: str,
        file_type: str | None = None,
        exclude_dirs: set[str] | None = None
) -> list[SearchMatch]:
    """在配置文件的 key 和 value 中搜索关键字。"""

    root = root.resolve()
    keyword_lower = keyword.lower()

    matches: list[SearchMatch] = []
    files = scan_config_files(root, file_type, exclude_dirs)

    for file in files:
        try:
            config = parse_config_file(file)
        except ValueError:
            # 当前 Parser 不支持的配置类型先跳过
            continue

        for key, value in config.items():
            key_text = key.lower()
            value_text = str(value).lower()

            if (keyword_lower in key_text or keyword_lower in value_text):
                matches.append(SearchMatch(file=file, key=key, value=value))

    return matches