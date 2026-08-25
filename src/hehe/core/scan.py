from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml
from hehe.core.parser import parse_config_file
from hehe.core.scanner import scan_config_files

SENSITIVE_KEYWORDS = {
    "password",
    "passwd",
    "pwd",
    "secret",
    "token",
    "api_key",
    "api-key",
    "apikey",
    "access_key",
    "access-key",
    "client_secret",
    "client-secret",
    "private_key",
    "private-key",
}

@dataclass
class SensitiveFinding:
    file: Path
    key: str
    value: Any
    keyword: str

def is_sensitive_key(key: str) -> str | None:
    """
      判断配置 key 是否属于敏感字段。

      只检查最后一级配置名称，避免：
      user.password.maxRetryCount
      user.password.lockTime
      这类配置被误判。
      """
    last_key = key.lower().split(".")[-1]

    # 去除常见分隔符
    normalized = (last_key.replace("-", "").replace("_", ""))

    for keyword in SENSITIVE_KEYWORDS:
        if normalized == keyword or normalized.endswith(keyword):
            return keyword
    return None

def scan_sensitive_configs(
        root: Path,
        file_type: str | None = None,
        exclude_dirs: set[str] | None = None
) -> list[SensitiveFinding]:
    """扫描配置文件中的敏感配置项。"""
    root = root.resolve()
    findings: list[SensitiveFinding] = []
    files = scan_config_files(root, file_type, exclude_dirs)

    for file in files:
        try:
            config = parse_config_file(file)
        except (ValueError, OSError, yaml.YAMLError):
            continue

        for key, value in config.items():
            # None 或空字符串没有实际敏感值，跳过
            if value is None:
                continue

            if isinstance(value, str) and not value.strip():
                continue

            keyword = is_sensitive_key(key)

            if keyword is None:
                continue

            findings.append(
                SensitiveFinding(
                    file=file,
                    key=key,
                    value=value,
                    keyword=keyword,
                )
            )
    return findings