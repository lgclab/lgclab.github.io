#!/usr/bin/env python3
"""Sync GitHub issue form submissions into Jekyll content files."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional


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


def find_member_by_name(root: Path, name: str) -> Optional[Path]:
    for path in sorted((root / "_members").glob("*.md")):
        content = path.read_text(encoding="utf-8")
        if extract_front_matter_value(content, "name") == name:
            return path
    return None


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
        normalized_value = raw_value.strip()
        if normalized_key in {"github", "email", "homepage", "scholar", "orcid"} and normalized_value:
            contact[normalized_key] = normalized_value
    return contact


def sync_member(root: Path, issue: Dict[str, object], fields: Dict[str, str]) -> SyncResult:
    name = clean_value(fields.get("姓名"))
    if not name:
        raise ValueError("成员 Issue 缺少姓名。")
    preferred_slug = slugify(clean_value(fields.get("成员页面文件名 slug")) or name, fallback="member")
    path = choose_member_path(root, preferred_slug, name)

    topics = lines_to_list(fields.get("研究主题 topics"))
    research = lines_to_list(fields.get("个人页展示的研究方向")) or topics
    contact_topics = lines_to_list(fields.get("可交流主题"))
    contact = parse_contact(fields.get("可公开联系方式"))
    open_to_contact = clean_value(fields.get("是否愿意公开连接入口")) != "否"
    status = clean_value(fields.get("状态")) or "其他"
    current = "课题组" if status == "在组" else status
    body = clean_value(fields.get("个人页正文")) or default_member_body(name, contact_topics)
    lines = [
        "---",
        yaml_scalar("name", name),
        yaml_scalar("title", name),
        yaml_scalar("cohort", clean_value(fields.get("入组或入学年份"))),
        yaml_scalar("role", clean_value(fields.get("身份"))),
        yaml_scalar("status", status),
        *yaml_list("research", research),
        *yaml_list("topics", topics),
        yaml_scalar("current", current),
        yaml_bool("open_to_contact", open_to_contact),
        *yaml_list("contact_topics", contact_topics),
        "contact:",
        f"  github: {yaml_quote(contact.get('github', ''))}",
        f"  email: {yaml_quote(contact.get('email', ''))}",
        "---",
        "",
        body,
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    rel_path = path.relative_to(root).as_posix()
    return SyncResult(rel_path, f"已同步成员信息到 `{rel_path}`。")


def default_member_body(name: str, contact_topics: List[str]) -> str:
    topics = "\n".join(f"- {topic}" for topic in contact_topics) if contact_topics else "- 可以补充可交流主题。"
    return "\n".join(
        [
            "## 我在做什么",
            "",
            f"这里可以补充{name}目前的研究方向、项目经历或正在关注的问题。",
            "",
            "## 可以找我聊什么",
            "",
            topics,
            "",
            "## 个人经验",
            "",
            "这里可以补充希望后来同学提前知道的经验。",
        ]
    )


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
