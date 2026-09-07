from dataclasses import dataclass
from pathlib import Path

import yaml
from yaml.nodes import MappingNode, SequenceNode, ScalarNode
from hehe.core.parser import parse_config_file, _normalize_yaml_content
from hehe.core.scanner import scan_config_files, get_config_type

@dataclass
class LintIssue:
    file: Path
    level: str
    message: str
    key: str | None=None


def lint_configs(
        root: Path,
        file_type: str | None=None,
        exclude_dirs: set[str] | None=None
) -> list[LintIssue]:
    """检查配置文件中的基础问题。"""
    root = root.resolve()
    issues: list[LintIssue] = []

    files = scan_config_files(root, file_type, exclude_dirs)

    for file in files:
        config_type = get_config_type(file)

        # YAML 重复key检测
        if config_type == "yaml" or config_type == "yml":
            try:
                issues.extend(_find_yaml_duplicate_keys(file))
            except yaml.YAMLError as ex:
                issues.append(LintIssue(file=file, level="ERROR", message=str(ex)))
                continue
        try:
            config = parse_config_file(file)

        except (ValueError, OSError, yaml.YAMLError) as ex:
            issues.append(
                LintIssue(
                    file=file,
                    level="ERROR",
                    message=str(ex)
                )
            )
            continue

        for key, value in config.items():

            # None
            if value is None:
                issues.append(
                    LintIssue(
                        file=file,
                        level="WARN",
                        key=key,
                        message="Empty value"
                    )
                )
                continue

            # ""
            if isinstance(value, str) and not value.strip():
                issues.append(
                    LintIssue(
                        file=file,
                        level="WARN",
                        key=key,
                        message="Empty value"
                    )
                )

    return issues

def _find_yaml_duplicate_keys(path: Path) -> list[LintIssue]:
    """查找 YAML 中的重复 Key"""
    content = path.read_text(encoding="utf-8-sig")

    # 兼容 @logging.level@ 这类 Maven 占位符
    content = _normalize_yaml_content(content)

    issues: list[LintIssue] = []

    for document in yaml.compose_all(content):
        if document is None:
            continue

        _walk_yaml_node(
            node=document,
            path=path,
            parent_key="",
            issues=issues
        )
    return issues

def _walk_yaml_node(
        node,
        path: Path,
        parent_key: str,
        issues: list[LintIssue]
) -> None:
    """递归检查 YAML AST"""

    if isinstance(node, MappingNode):
        seen_keys: set[str] = set()

        for key_node, value_node in node.value:
            if not isinstance(key_node, ScalarNode):
                continue

            key = str(key_node.value)
            full_key = (
                f"{parent_key}.{key}"
                if parent_key
                else key
            )

            if key in seen_keys:
                line_number = (key_node.start_mark.line + 1)
                issues.append(
                    LintIssue(
                        file=path,
                        level="ERROR",
                        key=full_key,
                        message=f"Duplicate key, line {line_number}",
                    )
                )
            else:
                seen_keys.add(key)

            _walk_yaml_node(
                node=value_node,
                path=path,
                parent_key=full_key,
                issues=issues
            )
    elif isinstance(node, SequenceNode):
        for index, item in enumerate(node.value):
            full_key = (
                f"{parent_key}[{index}]"
                if parent_key
                else f"[{index}]"
            )

            _walk_yaml_node(
                node=item,
                path=path,
                parent_key=full_key,
                issues=issues
            )