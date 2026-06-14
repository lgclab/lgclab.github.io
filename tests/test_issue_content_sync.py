import tempfile
import unittest
from pathlib import Path

from scripts import sync_issue_content
from scripts import update_member_issue_template


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


if __name__ == "__main__":
    unittest.main()
