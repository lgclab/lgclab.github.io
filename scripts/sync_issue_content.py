#!/usr/bin/env python3
"""Sync GitHub issue form submissions into Jekyll content files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional

try:
    from scripts import update_member_issue_template
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts import update_member_issue_template


NO_RESPONSE = "_No response_"


@dataclass
class SyncResult:
    changed_path: str
    comment: str


def parse_issue_form(body: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    current_label: Optional[str] = None
    current_lines: List[str] = []
    for line in body.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if match:
            if current_label is not None:
                fields[current_label] = "\n".join(current_lines).strip()
            current_label = match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_label is not None:
        fields[current_label] = "\n".join(current_lines).strip()
    return fields


def clean_value(value: Optional[str]) -> str:
    if not value:
        return ""
    value = value.strip()
    if value == NO_RESPONSE:
        return ""
    return value


def lines_to_list(value: Optional[str]) -> List[str]:
    cleaned = clean_value(value)
    if not cleaned:
        return []
    items = []
    for line in cleaned.splitlines():
        item = line.strip().strip("-").strip()
        if item and item != NO_RESPONSE:
            items.append(item)
    return unique(items)


def unique(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_scalar(key: str, value: str) -> str:
    return f"{key}: {yaml_quote(value)}"


def yaml_bool(key: str, value: bool) -> str:
    return f"{key}: {'true' if value else 'false'}"


def yaml_list(key: str, values: List[str]) -> List[str]:
    if not values:
        return [f"{key}: []"]
    lines = [f"{key}:"]
    lines.extend(f"  - {yaml_quote(value)}" for value in values)
    return lines


def yaml_contact(contact: Dict[str, str]) -> List[str]:
    contact_keys = ["github", "email", "homepage", "scholar", "orcid", "wechat", "substack"]
    entries = [(key, contact.get(key, "")) for key in contact_keys]
    entries = [(key, value) for key, value in entries if value]
    if not entries:
        return ["contact: {}"]
    lines = ["contact:"]
    lines.extend(f"  {key}: {yaml_quote(value)}" for key, value in entries)
    return lines


def slugify(value: str, fallback: str = "item") -> str:
    value = transliterate(value)
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or fallback


PINYIN = {
    "我": "wo",
    "的": "de",
    "开": "kai",
    "题": "ti",
    "经": "jing",
    "验": "yan",
    "刚": "gang",
    "入": "ru",
    "组": "zu",
    "前": "qian",
    "三": "san",
    "个": "ge",
    "月": "yue",
    "怎": "zen",
    "么": "me",
    "做": "zuo",
    "论": "lun",
    "文": "wen",
    "实": "shi",
    "验": "yan",
    "复": "fu",
    "现": "xian",
    "毕": "bi",
    "业": "ye",
    "流": "liu",
    "程": "cheng",
    "投": "tou",
    "稿": "gao",
    "测": "ce",
    "试": "shi",
    "贴": "tie",
}


def transliterate(value: str) -> str:
    parts = []
    for char in value:
        if char.isascii():
            parts.append(char)
        elif char in PINYIN:
            parts.append("-" + PINYIN[char] + "-")
        else:
            parts.append("-")
    return "".join(parts)


def extract_front_matter_value(content: str, key: str) -> str:
    if not content.startswith("---"):
        return ""
    match = re.search(rf"^{re.escape(key)}:\s*[\"']?(.+?)[\"']?\s*$", content, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def split_front_matter(content: str) -> tuple[str, str]:
    if not content.startswith("---\n"):
        return "", content
    _, rest = content.split("---\n", 1)
    front_matter, body = rest.split("\n---", 1)
    return front_matter, body.lstrip("\n")


def parse_front_matter(content: str) -> Dict[str, object]:
    front_matter, _ = split_front_matter(content)
    data: Dict[str, object] = {}
    current_list_key: Optional[str] = None
    current_map_key: Optional[str] = None
    for line in front_matter.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list_key:
            data.setdefault(current_list_key, [])
            item = line[4:].strip().strip('"')
            if isinstance(data[current_list_key], list):
                data[current_list_key].append(item)
            continue
        if line.startswith("  ") and current_map_key and ":" in line:
            key, value = line.strip().split(":", 1)
            data.setdefault(current_map_key, {})
            if isinstance(data[current_map_key], dict):
                data[current_map_key][key.strip()] = value.strip().strip('"')
            continue

        current_list_key = None
        current_map_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "contact":
            current_map_key = key
            data[key] = {}
        elif value == "":
            current_list_key = key
            data[key] = []
        elif value == "[]":
            data[key] = []
        elif value in {"true", "false"}:
            data[key] = value == "true"
        elif value == "{}":
            data[key] = {}
        else:
            data[key] = value.strip('"')
    return data


def read_member_page(path: Path) -> Dict[str, object]:
    content = path.read_text(encoding="utf-8")
    front_matter = parse_front_matter(content)
    _, body = split_front_matter(content)
    front_matter["body"] = body.rstrip()
    return front_matter


def list_value(value: object) -> List[str]:
    return value if isinstance(value, list) else []


def string_value(value: object) -> str:
    return value if isinstance(value, str) else ""


def bool_value(value: object, default: bool = True) -> bool:
    return value if isinstance(value, bool) else default


def contact_value(value: object) -> Dict[str, str]:
    return value if isinstance(value, dict) else {}


def find_member_by_name(root: Path, name: str) -> Optional[Path]:
    for path in sorted((root / "_members").glob("*.md")):
        content = path.read_text(encoding="utf-8")
        if extract_front_matter_value(content, "name") == name:
            return path
    return None


def find_member_by_slug(root: Path, slug: str) -> Optional[Path]:
    if not slug or slug == "不适用":
        return None
    path = root / "_members" / f"{slug}.md"
    return path if path.exists() else None


def choose_member_path(root: Path, preferred_slug: str, name: str) -> Path:
    members_dir = root / "_members"
    members_dir.mkdir(parents=True, exist_ok=True)
    existing_for_name = find_member_by_name(root, name)
    if existing_for_name is not None:
        return existing_for_name

    preferred = members_dir / f"{preferred_slug}.md"
    if not preferred.exists():
        return preferred

    existing_name = extract_front_matter_value(preferred.read_text(encoding="utf-8"), "name")
    if existing_name == name:
        return preferred

    index = 2
    while True:
        candidate = members_dir / f"{preferred_slug}-{index}.md"
        if not candidate.exists():
            return candidate
        candidate_name = extract_front_matter_value(candidate.read_text(encoding="utf-8"), "name")
        if candidate_name == name:
            return candidate
        index += 1


def parse_contact(value: Optional[str]) -> Dict[str, str]:
    contact = {}
    for line in lines_to_list(value):
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        normalized_key = key.strip().lower()
        normalized_value = normalize_contact_value(normalized_key, raw_value.strip())
        if normalized_key in {"github", "email", "homepage", "scholar", "orcid", "wechat", "substack"} and normalized_value:
            contact[normalized_key] = normalized_value
    return contact


def normalize_contact_value(key: str, value: str) -> str:
    markdown_link = re.match(r"^\[([^\]]+)\]\(([^)]+)\)$", value)
    if markdown_link:
        label, url = markdown_link.groups()
        value = label if key in {"github", "wechat", "orcid"} else url

    if key == "github":
        value = value.strip().removeprefix("@")
        value = re.sub(r"^https?://github\.com/", "", value)
        value = re.sub(r"^github\.com/", "", value)
        return value.strip("/")

    if key in {"homepage", "scholar", "substack"}:
        if value and not re.match(r"^https?://", value):
            value = "https://" + value
        return value

    return value


def sync_member(root: Path, issue: Dict[str, object], fields: Dict[str, str]) -> SyncResult:
    mode = clean_value(fields.get("提交类型")) or "新增成员"
    existing_slug = clean_value(fields.get("选择已有成员 slug"))
    existing_path = find_member_by_slug(root, existing_slug) if mode == "更新成员" else None
    if mode == "更新成员" and existing_path is None:
        raise ValueError("更新成员时需要选择一个已有成员 slug。")

    existing = read_member_page(existing_path) if existing_path else {}
    name = clean_value(fields.get("姓名")) or string_value(existing.get("name"))
    if not name:
        raise ValueError("成员 Issue 缺少姓名。")
    raw_slug = clean_value(fields.get("新成员页面文件名 slug")) or clean_value(fields.get("成员页面文件名 slug"))
    preferred_slug = slugify(raw_slug or name, fallback="member")
    path = existing_path or choose_member_path(root, preferred_slug, name)

    submitted_topics = lines_to_list(fields.get("研究主题 topics"))
    topics = submitted_topics or list_value(existing.get("topics"))
    submitted_research = lines_to_list(fields.get("个人页展示的研究方向"))
    research = submitted_research or list_value(existing.get("research")) or topics
    submitted_contact_topics = lines_to_list(fields.get("可交流主题"))
    contact_topics = submitted_contact_topics or list_value(existing.get("contact_topics"))
    submitted_contact = parse_contact(fields.get("可公开联系方式"))
    contact = submitted_contact or contact_value(existing.get("contact"))
    submitted_open_to_contact = clean_value(fields.get("是否愿意公开连接入口"))
    open_to_contact = bool_value(existing.get("open_to_contact")) if not submitted_open_to_contact else submitted_open_to_contact != "否"
    status = clean_value(fields.get("状态")) or string_value(existing.get("status")) or "其他"
    current = "课题组" if status == "在组" else status
    submitted_body = clean_value(fields.get("个人页正文"))
    submitted_about = clean_value(fields.get("我在做什么"))
    submitted_experience = clean_value(fields.get("个人经验"))
    existing_body = string_value(existing.get("body"))
    if submitted_body:
        body = submitted_body
    elif submitted_about or submitted_experience or not existing_body or is_generated_member_body(existing_body):
        body = default_member_body(name, contact_topics, research, submitted_about, submitted_experience)
    else:
        body = existing_body
    lines = [
        "---",
        yaml_scalar("name", name),
        yaml_scalar("title", name),
        yaml_scalar("cohort", clean_value(fields.get("入组或入学年份")) or string_value(existing.get("cohort"))),
        yaml_scalar("role", clean_value(fields.get("身份")) or string_value(existing.get("role"))),
        yaml_scalar("status", status),
        *yaml_list("research", research),
        *yaml_list("topics", topics),
        yaml_scalar("current", current),
        yaml_bool("open_to_contact", open_to_contact),
        *yaml_list("contact_topics", contact_topics),
        *yaml_contact(contact),
        "---",
        "",
        body,
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    template_path = root / ".github" / "ISSUE_TEMPLATE" / "member-update.yml"
    if template_path.exists():
        update_member_issue_template.update_template(root)
    rel_path = path.relative_to(root).as_posix()
    return SyncResult(rel_path, f"已同步成员信息到 `{rel_path}`。")


def markdown_list(values: List[str], placeholder: str) -> str:
    return "\n".join(f"- {value}" for value in values) if values else placeholder


def is_generated_member_body(body: str) -> bool:
    required_headings = ["## 我在做什么", "## 可以找我聊什么", "## 个人经验"]
    if not all(heading in body for heading in required_headings):
        return False
    generated_phrases = ["这里可以补充", "- 可以补充可交流主题。"]
    return any(phrase in body for phrase in generated_phrases) or "## 研究方向" in body


def default_member_body(
    name: str,
    contact_topics: List[str],
    research: List[str],
    about: str = "",
    experience: str = "",
) -> str:
    sections: List[str] = []
    if research:
        sections.extend(
            [
                "## 研究方向",
                "",
                markdown_list(research, ""),
                "",
            ]
        )
    about_text = about or markdown_list(
        research,
        f"这里可以补充{name}目前的研究方向、项目经历或正在关注的问题。",
    )
    topics = markdown_list(contact_topics, "- 可以补充可交流主题。")
    experience_text = experience or "这里可以补充希望后来同学提前知道的经验。"
    sections.extend(
        [
            "## 我在做什么",
            "",
            about_text,
            "",
            "## 可以找我聊什么",
            "",
            topics,
            "",
            "## 个人经验",
            "",
            experience_text,
        ]
    )
    return "\n".join(sections)


def find_post_by_issue_number(root: Path, issue_number: object) -> Optional[Path]:
    expected = str(issue_number)
    for path in sorted((root / "_posts").glob("*.md")):
        content = path.read_text(encoding="utf-8")
        if extract_front_matter_value(content, "issue_number") == expected:
            return path
    return None


def unique_post_path(root: Path, date_string: str, title: str) -> Path:
    posts_dir = root / "_posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(title, fallback="post")
    path = posts_dir / f"{date_string}-{slug}.md"
    if not path.exists():
        return path
    index = 2
    while True:
        candidate = posts_dir / f"{date_string}-{slug}-{index}.md"
        if not candidate.exists():
            return candidate
        index += 1


def sync_post(root: Path, issue: Dict[str, object], fields: Dict[str, str], today: str) -> SyncResult:
    title = clean_value(fields.get("标题"))
    if not title:
        raise ValueError("经验贴 Issue 缺少标题。")
    issue_number = issue.get("number", "")
    existing = find_post_by_issue_number(root, issue_number)
    path = existing or unique_post_path(root, today, title)

    category = clean_value(fields.get("分类")) or "经验贴"
    tags = lines_to_list(fields.get("标签 tags"))
    topics = unique([category] + tags)
    body = clean_value(fields.get("正文")) or "## 正文\n\n请补充经验贴内容。"

    lines = [
        "---",
        yaml_scalar("title", title),
        yaml_scalar("author", clean_value(fields.get("作者"))),
        f"date: {today}",
        yaml_scalar("category", category),
        *yaml_list("topics", topics),
        *yaml_list("tags", tags),
        yaml_scalar("audience", clean_value(fields.get("适合谁读"))),
        f"issue_number: {issue_number}",
        "---",
        "",
        body,
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    rel_path = path.relative_to(root).as_posix()
    return SyncResult(rel_path, f"已同步经验贴到 `{rel_path}`。")


def sync_issue(root: Path, issue: Dict[str, object], today: Optional[str] = None) -> SyncResult:
    today = today or date.today().isoformat()
    title = str(issue.get("title", ""))
    body = str(issue.get("body", ""))
    fields = parse_issue_form(body)
    if title.startswith("[成员]"):
        return sync_member(root, issue, fields)
    if title.startswith("[经验贴]"):
        return sync_post(root, issue, fields, today)
    raise ValueError("只支持标题以 [成员] 或 [经验贴] 开头的 Issue。")


def load_issue_from_event(event_path: Path) -> Dict[str, object]:
    event = json.loads(event_path.read_text(encoding="utf-8"))
    issue = event.get("issue")
    if not isinstance(issue, dict):
        raise ValueError("GitHub event 中没有 issue 对象。")
    return issue


def write_comment_json(path: Path, body: str) -> None:
    path.write_text(json.dumps({"body": body}, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True, help="Path to the GitHub event JSON file.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--comment-json", default="issue-sync-comment.json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    issue = load_issue_from_event(Path(args.event))
    result = sync_issue(root, issue)
    comment = result.comment + "\n\n如果需要调整内容，可以继续编辑这个 Issue，自动同步会重新运行。"
    write_comment_json(root / args.comment_json, comment)
    print(result.changed_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
