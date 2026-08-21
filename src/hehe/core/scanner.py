import os
from pathlib import Path

# 默认忽略的目录
IGNORE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "node_modules",
    "target",
    "dist",
    "build",
    "__pycache__",
}

# 常见配置文件扩展名
CONFIG_SUFFIXES = {
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".properties",
    ".ini",
    ".cfg",
    ".conf",
    ".env"
}

# 特殊配置文件名称
CONFIG_FILENAMES = {
    "pyproject.toml",
    "package.json",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
}

def is_config_file(path: Path) -> bool:
    """判断一个文件是否属于配置文件。"""
    name = path.name.lower()

    # .env / .env.dev / .env.prod
    if name == ".env" or name.startswith(".env."):
        return True
    if name in CONFIG_FILENAMES:
        return True
    return path.suffix.lower() in CONFIG_SUFFIXES

def scan_config_files(
        root:Path,
        file_type: str | None = None,
        exclude_dirs: set[str] | None = None,
) -> list[Path]:
    """递归扫描目录中的配置文件。"""

    root = root.resolve()
    result:list[Path] = []

    # 默认忽略目录 + 用户指定目录
    ignored = IGNORE_DIRS.copy()

    if exclude_dirs:
        ignored.update(exclude_dirs)

    for current_dir, dirs, files in os.walk(root):
        # 直接阻止os.walk进入这些目录
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in ignored
        ]

        for filename in files:
            path = Path(current_dir) / filename

            if not is_config_file(path):
                continue

            if file_type and get_config_type(path) != file_type.lower():
                continue

            result.append(path)

    return sorted(result)

def get_config_type(path: Path) -> str:
    """获取配置文件类型。"""
    name = path.name.lower()

    if name == ".env" or name.startswith(".env."):
        return "env"
    suffix_map = {
        ".yml": "yaml",
        ".yaml": "yaml",
        ".json": "json",
        ".toml": "toml",
        ".properties": "properties",
        ".ini": "ini",
        ".cfg": "cfg",
        ".conf": "conf",
    }
    return suffix_map.get(path.suffix.lower(), "unkonw")