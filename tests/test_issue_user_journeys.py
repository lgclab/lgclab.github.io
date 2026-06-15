import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import sync_issue_content

ROOT = Path(__file__).resolve().parents[1]


def form_body(fields):
    return "\n\n".join(f"### {label}\n\n{value}" for label, value in fields)


def read(path):
    return path.read_text(encoding="utf-8")


class IssueUserJourneyTest(unittest.TestCase):
    def make_root(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "_members").mkdir()
        (root / "_posts").mkdir()
        template_dir = root / ".github" / "ISSUE_TEMPLATE"
        template_dir.mkdir(parents=True)
        shutil.copy(
            ROOT / ".github" / "ISSUE_TEMPLATE" / "member-update.yml",
            template_dir / "member-update.yml",
        )
        self.addCleanup(tmp.cleanup)
        return root

    def write_existing_member(self, root, slug="li-ming"):
        path = root / "_members" / f"{slug}.md"
        path.write_text(
            "\n".join(
                [
                    "---",
                    'name: "李明"',
                    'title: "李明"',
                    'cohort: "2024"',
                    'role: "硕士"',
                    'status: "在组"',
                    "research:",
                    '  - "旧方向"',
                    "topics:",
                    '  - "旧主题"',
                    'current: "课题组"',
                    "open_to_contact: true",
                    "contact_topics:",
                    '  - "旧交流"',
                    "contact:",
                    '  github: "old-gh"',
                    "---",
                    "",
                    "## 我在做什么",
                    "",
                    "- 旧方向",
                    "",
                    "## 可以找我聊什么",
                    "",
                    "- 旧交流",
                    "",
                    "## 个人经验",
                    "",
                    "旧经验。",
                ]
            ),
            encoding="utf-8",
        )
        return path

    def test_user_can_add_member_and_site_can_surface_member_everywhere(self):
        root = self.make_root()
        issue = {
            "number": 101,
            "title": "[成员] 陈晨",
            "body": form_body(
                [
                    ("提交类型", "新增成员"),
                    ("选择已有成员 slug", "不适用"),
                    ("姓名", "陈晨"),
                    ("新成员页面文件名 slug", "chen-chen"),
                    ("入组或入学年份", "2026"),
                    ("身份", "博士"),
                    ("状态", "在组"),
                    ("研究主题 topics", "多智能体系统\n强化学习"),
                    ("个人页展示的研究方向", "多智能体协作\nAgent Context Infrastructure"),
                    ("我在做什么", "研究多智能体协作中的信用分配。"),
                    ("可交流主题", "开题准备\n实验复现"),
                    ("个人经验", "刚入组时先跑通一个 baseline。"),
                    ("是否愿意公开连接入口", "是"),
                    (
                        "可公开联系方式",
                        "Github: [@chen-lab](github.com/chen-lab)\nHomepage: https://chen.example.com\nScholar: https://scholar.example.com/chen\nORCID: 0000-0000-0000-0001\nWeChat: chen-lab\nSubstack: [chen.substack.com](chen.substack.com)",
                    ),
                    ("个人页正文", "_No response_"),
                ]
            ),
        }

        result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

        self.assertEqual(result.changed_path, "_members/chen-chen.md")
        member_content = read(root / result.changed_path)
        self.assertIn('name: "陈晨"', member_content)
        self.assertIn('cohort: "2026"', member_content)
        self.assertIn('status: "在组"', member_content)
        self.assertIn('current: "课题组"', member_content)
        self.assertIn('  - "多智能体系统"', member_content)
        self.assertIn('  - "强化学习"', member_content)
        self.assertIn('  - "多智能体协作"', member_content)
        self.assertIn('  - "Agent Context Infrastructure"', member_content)
        self.assertIn('github: "chen-lab"', member_content)
        self.assertIn('homepage: "https://chen.example.com"', member_content)
        self.assertIn('scholar: "https://scholar.example.com/chen"', member_content)
        self.assertIn('orcid: "0000-0000-0000-0001"', member_content)
        self.assertIn('wechat: "chen-lab"', member_content)
        self.assertIn('substack: "https://chen.substack.com"', member_content)
        self.assertIn("## 研究方向", member_content)
        self.assertIn("- 多智能体协作", member_content)
        self.assertIn("- Agent Context Infrastructure", member_content)
        self.assertIn("研究多智能体协作中的信用分配。", member_content)
        self.assertIn("- 开题准备", member_content)
        self.assertIn("刚入组时先跑通一个 baseline。", member_content)

        generated_template = read(root / ".github" / "ISSUE_TEMPLATE" / "member-update.yml")
        self.assertIn("        - chen-chen", generated_template)

        members_page = read(ROOT / "members.md")
        member_layout = read(ROOT / "_layouts" / "member.html")
        topics_page = read(ROOT / "topics.md")
        self.assertIn("site.members", members_page)
        self.assertIn("member.url", members_page)
        self.assertIn("member.topics", members_page)
        self.assertNotIn("member.research", members_page)
        self.assertIn("member.contact_topics", members_page)
        self.assertIn("member.contact.homepage", members_page)
        self.assertIn("member.contact.scholar", members_page)
        self.assertIn("member.contact.orcid", members_page)
        self.assertIn("member.contact.wechat", members_page)
        self.assertIn("member.contact.substack", members_page)
        self.assertIn("{{ content }}", member_layout)
        self.assertIn("page.topics", member_layout)
        self.assertNotIn("page.research", member_layout)
        self.assertIn("page.contact.homepage", member_layout)
        self.assertIn("page.contact.scholar", member_layout)
        self.assertIn("page.contact.orcid", member_layout)
        self.assertIn("page.contact.wechat", member_layout)
        self.assertIn("page.contact.substack", member_layout)
        self.assertIn("member.topics", topics_page)
        self.assertIn("member.url", topics_page)

    def test_deleted_member_does_not_leave_stale_theme_or_dropdown_entries(self):
        root = self.make_root()
        self.write_existing_member(root, slug="zhang-san")
        template = root / ".github" / "ISSUE_TEMPLATE" / "member-update.yml"
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
                    "        - zhang-san",
                    "        # member-slug-options:end",
                ]
            ),
            encoding="utf-8",
        )

        (root / "_members" / "zhang-san.md").unlink()
        from scripts import update_member_issue_template

        update_member_issue_template.update_template(root)

        generated_template = read(template)
        self.assertNotIn("zhang-san", generated_template)

        workflow = read(ROOT / ".github" / "workflows" / "member-template-sync.yml")
        self.assertIn("_members/**", workflow)
        self.assertIn("scripts/update_member_issue_template.py", workflow)

        topics_page = read(ROOT / "topics.md")
        self.assertIn("site.members", topics_page)
        self.assertIn("member.topics", topics_page)
        self.assertIn("member.url", topics_page)

    def test_user_can_update_existing_member_without_creating_duplicate(self):
        root = self.make_root()
        self.write_existing_member(root)
        issue = {
            "number": 102,
            "title": "[成员] 更新李明",
            "body": form_body(
                [
                    ("提交类型", "更新成员"),
                    ("选择已有成员 slug", "li-ming"),
                    ("姓名", "_No response_"),
                    ("新成员页面文件名 slug", "_No response_"),
                    ("入组或入学年份", "_No response_"),
                    ("身份", "_No response_"),
                    ("状态", "已毕业"),
                    ("研究主题 topics", "多模态学习"),
                    ("个人页展示的研究方向", "多模态学习"),
                    ("我在做什么", "目前关注多模态模型评估。"),
                    ("可交流主题", "毕业流程\n求职准备"),
                    ("个人经验", "毕业前提前确认材料清单。"),
                    ("是否愿意公开连接入口", "_No response_"),
                    ("可公开联系方式", "_No response_"),
                    ("个人页正文", "_No response_"),
                ]
            ),
        }

        result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

        self.assertEqual(result.changed_path, "_members/li-ming.md")
        self.assertEqual(sorted(path.name for path in (root / "_members").glob("*.md")), ["li-ming.md"])
        member_content = read(root / "_members" / "li-ming.md")
        self.assertIn('name: "李明"', member_content)
        self.assertIn('cohort: "2024"', member_content)
        self.assertIn('role: "硕士"', member_content)
        self.assertIn('status: "已毕业"', member_content)
        self.assertIn('current: "已毕业"', member_content)
        self.assertIn('  - "多模态学习"', member_content)
        self.assertIn('github: "old-gh"', member_content)
        self.assertIn("目前关注多模态模型评估。", member_content)
        self.assertIn("- 毕业流程", member_content)
        self.assertIn("毕业前提前确认材料清单。", member_content)

    def test_user_can_add_experience_post_and_site_can_surface_post_everywhere(self):
        root = self.make_root()
        issue = {
            "number": 201,
            "title": "[经验贴] 刚入组前三个月怎么做",
            "body": form_body(
                [
                    ("标题", "刚入组前三个月怎么做"),
                    ("作者", "陈晨"),
                    ("分类", "入组指南"),
                    ("标签 tags", "科研启动\n论文阅读\n实验复现"),
                    ("适合谁读", "新入组同学"),
                    ("正文", "## 背景\n\n前三个月先建立节奏。\n\n## 常见坑\n\n不要同时开太多方向。"),
                ]
            ),
        }

        result = sync_issue_content.sync_issue(root, issue, today="2026-06-14")

        self.assertEqual(result.changed_path, "_posts/2026-06-14-gang-ru-zu-qian-san-ge-yue-zen-me-zuo.md")
        post_content = read(root / result.changed_path)
        self.assertIn('title: "刚入组前三个月怎么做"', post_content)
        self.assertIn('author: "陈晨"', post_content)
        self.assertIn('category: "入组指南"', post_content)
        self.assertIn("topics:\n  - \"入组指南\"\n  - \"科研启动\"\n  - \"论文阅读\"\n  - \"实验复现\"", post_content)
        self.assertIn("tags:\n  - \"科研启动\"\n  - \"论文阅读\"\n  - \"实验复现\"", post_content)
        self.assertIn('audience: "新入组同学"', post_content)
        self.assertIn("issue_number: 201", post_content)
        self.assertIn("前三个月先建立节奏。", post_content)

        posts_page = read(ROOT / "posts.md")
        post_layout = read(ROOT / "_layouts" / "post.html")
        topics_page = read(ROOT / "topics.md")
        self.assertIn("site.posts", posts_page)
        self.assertIn("post.url", posts_page)
        self.assertIn("post.category", posts_page)
        self.assertIn("post.tags", posts_page)
        self.assertIn("{{ content }}", post_layout)
        self.assertIn("page.category", post_layout)
        self.assertIn("page.tags", post_layout)
        self.assertIn("post.topics", topics_page)
        self.assertIn("post.url", topics_page)

    def test_user_can_update_existing_experience_post_by_editing_original_issue(self):
        root = self.make_root()
        original_issue = {
            "number": 202,
            "title": "[经验贴] 投稿经验",
            "body": form_body(
                [
                    ("标题", "投稿经验"),
                    ("作者", "李明"),
                    ("分类", "投稿经验"),
                    ("标签 tags", "初稿\n返修"),
                    ("适合谁读", "准备投稿的同学"),
                    ("正文", "## 背景\n\n旧内容。"),
                ]
            ),
        }
        first = sync_issue_content.sync_issue(root, original_issue, today="2026-06-14")

        edited_issue = {
            "number": 202,
            "title": "[经验贴] 投稿经验",
            "body": form_body(
                [
                    ("标题", "投稿经验更新版"),
                    ("作者", "李明"),
                    ("分类", "投稿复盘"),
                    ("标签 tags", "返修\n审稿意见"),
                    ("适合谁读", "正在返修的同学"),
                    ("正文", "## 背景\n\n更新后的内容。"),
                ]
            ),
        }
        second = sync_issue_content.sync_issue(root, edited_issue, today="2026-06-15")

        self.assertEqual(second.changed_path, first.changed_path)
        self.assertEqual(len(list((root / "_posts").glob("*.md"))), 1)
        post_content = read(root / second.changed_path)
        self.assertIn('title: "投稿经验更新版"', post_content)
        self.assertIn('category: "投稿复盘"', post_content)
        self.assertIn("topics:\n  - \"投稿复盘\"\n  - \"返修\"\n  - \"审稿意见\"", post_content)
        self.assertIn('audience: "正在返修的同学"', post_content)
        self.assertIn("更新后的内容。", post_content)
        self.assertNotIn("旧内容。", post_content)

    def test_issue_mechanism_is_documented_for_maintainers_and_users(self):
        readme = read(ROOT / "README.md")
        contributing = read(ROOT / "CONTRIBUTING.md")
        log = ROOT / "docs" / "issue-mechanism-test-log.md"

        self.assertIn("我在做什么", readme)
        self.assertIn("个人经验", readme)
        self.assertIn("GitHub、个人主页、Google Scholar、ORCID", readme)
        self.assertIn("编辑原 Issue", contributing)
        self.assertTrue(log.is_file(), "Issue mechanism test log should document the audited user journeys.")
        log_content = read(log)
        self.assertIn("新增成员", log_content)
        self.assertIn("更新成员", log_content)
        self.assertIn("新增经验贴", log_content)
        self.assertIn("更新经验贴", log_content)
        self.assertIn("docs/issue-mechanism-test-log.md", read(ROOT / "_config.yml"))


if __name__ == "__main__":
    unittest.main()
