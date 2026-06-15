import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import sync_issue_content
from scripts import update_member_issue_template

ROOT = Path(__file__).resolve().parents[1]


def form_body(fields):
    parts = []
    for label, value in fields:
        parts.append(f"### {label}\n\n{value}")
    return "\n\n".join(parts)


class IssueContentSyncTest(unittest.TestCase):
    def write_member(self, root, slug, name):
        members_dir = root / "_members"
        members_dir.mkdir(parents=True, exist_ok=True)
        (members_dir / f"{slug}.md").write_text(
            "\n".join(
                [
                    "---",
                    f'name: "{name}"',
                    f'title: "{name}"',
                    'cohort: "2024"',
                    'role: "硕士"',
                    'status: "在组"',
                    "topics:",
                    '  - "旧主题"',
                    "open_to_contact: true",
                    "contact_topics:",
                    '  - "旧交流"',
                    "contact:",
                    '  github: "old-gh"',
                    '  email: "old@example.com"',
                    "---",
                    "",
                    "旧正文",
                ]
            ),
            encoding="utf-8",
        )

    def test_member_issue_updates_existing_file_when_slug_and_name_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_member(root, "zhang-san", "张三")
            issue = {
                "number": 1,
                "title": "[成员] 张三",
                "body": form_body(
                    [
                        ("姓名", "张三"),
                        ("成员页面文件名 slug", "Zhang san"),
                        ("入组或入学年份", "2028"),
                        ("身份", "博士"),
                        ("状态", "在组"),
                        ("研究主题 topics", "你好\n我好\n大家好"),
                        ("个人页展示的研究方向", "_No response_"),
                        ("可交流主题", "_No response_"),
                        ("是否愿意公开连接入口", "是"),
                        ("可公开联系方式", "_No response_"),
                        ("个人页正文", "_No response_"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

            self.assertEqual(result.changed_path, "_members/zhang-san.md")
            content = (root / "_members/zhang-san.md").read_text(encoding="utf-8")
            self.assertIn('cohort: "2028"', content)
            self.assertIn('role: "博士"', content)
            self.assertIn('  - "你好"', content)
            self.assertNotIn("旧主题", content)
            self.assertNotIn("由 GitHub Issue", content)

    def test_member_issue_update_mode_uses_selected_slug_and_preserves_blank_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_member(root, "zhang-san", "张三")
            issue = {
                "number": 4,
                "title": "[成员] 更新张三",
                "body": form_body(
                    [
                        ("提交类型", "更新成员"),
                        ("选择已有成员 slug", "zhang-san"),
                        ("姓名", "_No response_"),
                        ("新成员页面文件名 slug", "_No response_"),
                        ("入组或入学年份", "2029"),
                        ("身份", "_No response_"),
                        ("状态", "_No response_"),
                        ("研究主题 topics", "新主题"),
                        ("个人页展示的研究方向", "_No response_"),
                        ("可交流主题", "_No response_"),
                        ("是否愿意公开连接入口", "_No response_"),
                        ("可公开联系方式", "_No response_"),
                        ("个人页正文", "_No response_"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

            self.assertEqual(result.changed_path, "_members/zhang-san.md")
            content = (root / "_members/zhang-san.md").read_text(encoding="utf-8")
            self.assertIn('name: "张三"', content)
            self.assertIn('cohort: "2029"', content)
            self.assertIn('role: "硕士"', content)
            self.assertIn('status: "在组"', content)
            self.assertIn('  - "新主题"', content)
            self.assertIn('  - "旧交流"', content)
            self.assertIn('github: "old-gh"', content)
            self.assertIn("旧正文", content)

    def test_member_issue_blank_body_uses_research_in_profile_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue = {
                "number": 5,
                "title": "[成员] 王五",
                "body": form_body(
                    [
                        ("提交类型", "新增成员"),
                        ("选择已有成员 slug", "不适用"),
                        ("姓名", "王五"),
                        ("新成员页面文件名 slug", "wang-wu"),
                        ("入组或入学年份", "2030"),
                        ("身份", "硕士"),
                        ("状态", "已毕业"),
                        ("研究主题 topics", "AI agents"),
                        ("个人页展示的研究方向", "相约1829"),
                        ("可交流主题", "吃饭，唱歌，玩耍"),
                        ("是否愿意公开连接入口", "是"),
                        ("可公开联系方式", "_No response_"),
                        ("个人页正文", "_No response_"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

            content = (root / result.changed_path).read_text(encoding="utf-8")
            self.assertIn("## 我在做什么", content)
            self.assertIn("- 相约1829", content)
            self.assertIn("- 吃饭，唱歌，玩耍", content)
            self.assertNotIn("这里可以补充王五目前的研究方向", content)

    def test_member_issue_omits_blank_contact_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue = {
                "number": 7,
                "title": "[成员] 钱七",
                "body": form_body(
                    [
                        ("提交类型", "新增成员"),
                        ("选择已有成员 slug", "不适用"),
                        ("姓名", "钱七"),
                        ("新成员页面文件名 slug", "qian-qi"),
                        ("入组或入学年份", "2032"),
                        ("身份", "硕士"),
                        ("状态", "在组"),
                        ("研究主题 topics", "控制"),
                        ("个人页展示的研究方向", "控制"),
                        ("可交流主题", "复现"),
                        ("是否愿意公开连接入口", "是"),
                        ("可公开联系方式", "_No response_"),
                        ("个人页正文", "_No response_"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

            content = (root / result.changed_path).read_text(encoding="utf-8")
            self.assertIn("contact: {}", content)
            self.assertNotIn('github: ""', content)
            self.assertNotIn('email: ""', content)

    def test_member_issue_section_fields_build_profile_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue = {
                "number": 6,
                "title": "[成员] 赵六",
                "body": form_body(
                    [
                        ("提交类型", "新增成员"),
                        ("选择已有成员 slug", "不适用"),
                        ("姓名", "赵六"),
                        ("新成员页面文件名 slug", "zhao-liu"),
                        ("入组或入学年份", "2031"),
                        ("身份", "博士"),
                        ("状态", "在组"),
                        ("研究主题 topics", "机器人"),
                        ("个人页展示的研究方向", "具身智能"),
                        ("我在做什么", "最近在做具身智能实验。"),
                        ("可交流主题", "实验复现"),
                        ("个人经验", "开题前可以先把 baseline 跑通。"),
                        ("是否愿意公开连接入口", "否"),
                        ("可公开联系方式", "_No response_"),
                        ("个人页正文", "_No response_"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

            content = (root / result.changed_path).read_text(encoding="utf-8")
            self.assertIn("最近在做具身智能实验。", content)
            self.assertIn("- 实验复现", content)
            self.assertIn("开题前可以先把 baseline 跑通。", content)

    def test_member_issue_creates_unique_slug_when_slug_exists_for_different_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_member(root, "zhang-san", "张三")
            issue = {
                "number": 2,
                "title": "[成员] 章散",
                "body": form_body(
                    [
                        ("姓名", "章散"),
                        ("成员页面文件名 slug", "zhang san"),
                        ("入组或入学年份", "2028"),
                        ("身份", "博士"),
                        ("状态", "在组"),
                        ("研究主题 topics", "图学习"),
                        ("个人页展示的研究方向", "图学习"),
                        ("可交流主题", "选题"),
                        ("是否愿意公开连接入口", "否"),
                        ("可公开联系方式", "_No response_"),
                        ("个人页正文", "## 我在做什么\n\n研究图学习。"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

            self.assertEqual(result.changed_path, "_members/zhang-san-2.md")
            self.assertTrue((root / "_members/zhang-san.md").is_file())
            new_content = (root / "_members/zhang-san-2.md").read_text(encoding="utf-8")
            self.assertIn('name: "章散"', new_content)
            self.assertIn("open_to_contact: false", new_content)

    def test_post_issue_supports_custom_category_tags_and_topics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue = {
                "number": 3,
                "title": "[经验贴] 我的开题经验",
                "body": form_body(
                    [
                        ("标题", "我的开题经验"),
                        ("作者", "张三"),
                        ("分类", "开题复盘"),
                        ("标签 tags", "开题\n选题\n文献阅读"),
                        ("适合谁读", "准备开题的同学"),
                        ("正文", "## 背景\n\n一些经验。"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

            self.assertEqual(result.changed_path, "_posts/2026-06-14-wo-de-kai-ti-jing-yan.md")
            content = (root / result.changed_path).read_text(encoding="utf-8")
            self.assertIn('category: "开题复盘"', content)
            self.assertIn("tags:\n  - \"开题\"\n  - \"选题\"\n  - \"文献阅读\"", content)
            self.assertIn("topics:\n  - \"开题复盘\"\n  - \"开题\"\n  - \"选题\"\n  - \"文献阅读\"", content)

    def test_post_issue_uses_pinyin_slug_for_test_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue = {
                "number": 5,
                "title": "[经验贴] 测试贴",
                "body": form_body(
                    [
                        ("标题", "测试"),
                        ("作者", "刘倍延"),
                        ("分类", "投稿经验"),
                        ("标签 tags", "_No response_"),
                        ("适合谁读", "_No response_"),
                        ("正文", "你好"),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-15")

            self.assertEqual(result.changed_path, "_posts/2026-06-15-ce-shi.md")
            self.assertTrue((root / result.changed_path).is_file())

    def test_post_issue_preserves_markdown_h3_headings_in_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            issue = {
                "number": 7,
                "title": "[经验贴] 廖老板小组生存指南",
                "body": form_body(
                    [
                        ("标题", "廖老板小组生存指南"),
                        ("作者", "刘倍延"),
                        ("分类", "组内指南"),
                        ("标签 tags", "组内指南"),
                        ("适合谁读", "新入组同学"),
                        (
                            "正文",
                            "## 组会和论文分享\n\n我们组的组会包括两部分。\n\n### 组会\n\n- 保持诚实。\n\n### 标题\n\n这个小标题不应被误判成表单字段。\n\n### 论文分享\n\n- 每个人都要提问。",
                        ),
                    ]
                ),
            }

            result = sync_issue_content.sync_issue(root, issue, today="2026-06-15")

            content = (root / result.changed_path).read_text(encoding="utf-8")
            self.assertIn("### 组会", content)
            self.assertIn("- 保持诚实。", content)
            self.assertIn("### 标题", content)
            self.assertIn("这个小标题不应被误判成表单字段。", content)
            self.assertIn("### 论文分享", content)
            self.assertIn("- 每个人都要提问。", content)

    def test_member_issue_template_dropdown_is_generated_from_member_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_member(root, "zhang-san", "张三")
            self.write_member(root, "li-si", "李四")
            template = root / ".github" / "ISSUE_TEMPLATE" / "member-update.yml"
            template.parent.mkdir(parents=True)
            template.write_text(
                "\n".join(
                    [
                        "body:",
                        "  - type: dropdown",
                        "    id: existing_slug",
                        "    attributes:",
                        "      label: 选择已有成员 slug",
                        "      options:",
                        "        # member-slug-options:start",
                        "        - 不适用",
                        "        # member-slug-options:end",
                    ]
                ),
                encoding="utf-8",
            )

            update_member_issue_template.update_template(root)

            content = template.read_text(encoding="utf-8")
            self.assertIn("        - li-si", content)
            self.assertIn("        - zhang-san", content)
            self.assertLess(content.index("- li-si"), content.index("- zhang-san"))

    def test_sync_script_runs_as_workflow_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_path = root / "event.json"
            event_path.write_text(
                json.dumps(
                    {
                        "issue": {
                            "number": 3,
                            "title": "[成员] 王五",
                            "body": form_body(
                                [
                                    ("提交类型", "新增成员"),
                                    ("选择已有成员 slug", "不适用"),
                                    ("姓名", "王五"),
                                    ("新成员页面文件名 slug", "wang-wu"),
                                    ("入组或入学年份", "2030"),
                                    ("身份", "硕士"),
                                    ("状态", "已毕业"),
                                    ("研究主题 topics", "_No response_"),
                                    ("个人页展示的研究方向", "_No response_"),
                                    ("可交流主题", "_No response_"),
                                    ("是否愿意公开连接入口", "是"),
                                    ("可公开联系方式", "_No response_"),
                                    ("个人页正文", "_No response_"),
                                ]
                            ),
                        }
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "sync_issue_content.py"),
                    "--event",
                    str(event_path),
                    "--root",
                    str(root),
                    "--comment-json",
                    "comment.json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "_members" / "wang-wu.md").is_file())

    def test_member_templates_do_not_render_blank_contact_as_empty_github_link(self):
        self.assertIn(
            "member.contact.github != blank",
            (ROOT / "members.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "page.contact.github != blank",
            (ROOT / "_layouts" / "member.html").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
