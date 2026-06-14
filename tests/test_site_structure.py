import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteStructureTest(unittest.TestCase):
    def assert_file_contains(self, relative_path, expected_text):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"Missing file: {relative_path}")
        content = path.read_text(encoding="utf-8")
        self.assertIn(expected_text, content, f"{relative_path} should contain {expected_text!r}")

    def assert_file_not_contains(self, relative_path, unexpected_text):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"Missing file: {relative_path}")
        content = path.read_text(encoding="utf-8")
        self.assertNotIn(unexpected_text, content, f"{relative_path} should not contain {unexpected_text!r}")

    def test_required_top_level_pages_exist(self):
        for relative_path in [
            "_config.yml",
            "index.md",
            "posts.md",
            "members.md",
            "topics.md",
            "about.md",
        ]:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), f"Missing file: {relative_path}")

    def test_site_has_core_sections(self):
        self.assert_file_contains("index.md", "经验贴")
        self.assert_file_contains("index.md", "成员连接")
        self.assert_file_contains("posts.md", "site.posts")
        self.assert_file_contains("members.md", "site.members")
        self.assert_file_contains("topics.md", "site.posts")
        self.assert_file_contains("topics.md", "site.members")
        self.assert_file_contains("about.md", "如何参与维护")

    def test_layouts_and_styles_exist(self):
        for relative_path in [
            "_layouts/default.html",
            "_layouts/page.html",
            "_layouts/post.html",
            "_layouts/member.html",
            "assets/css/site.css",
        ]:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), f"Missing file: {relative_path}")

    def test_members_are_maintained_as_markdown_pages(self):
        self.assert_file_contains("_config.yml", "members:")
        self.assert_file_contains("_config.yml", "permalink: /members/:name/")
        self.assert_file_contains("members.md", "site.members")
        self.assert_file_contains("members.md", "member.url")
        self.assert_file_contains("_members/zhang-san.md", "open_to_contact")
        self.assert_file_contains("_members/zhang-san.md", "contact_topics")
        self.assert_file_contains("_members/zhang-san.md", "topics:")
        self.assert_file_contains("_members/zhang-san.md", "## 我在做什么")
        self.assert_file_contains("_layouts/member.html", "page.contact_topics")

    def test_members_page_uses_one_unified_member_list(self):
        self.assert_file_contains("members.md", "## 成员列表")
        self.assert_file_not_contains("members.md", "## 当前成员")
        self.assert_file_not_contains("members.md", "## 毕业成员")
        self.assert_file_not_contains("members.md", 'member.status == "在组"')
        self.assert_file_not_contains("members.md", 'member.status != "在组"')

    def test_topics_are_aggregated_from_posts_and_members(self):
        self.assertFalse((ROOT / "_data/topics.yml").exists())
        self.assert_file_contains("_posts/2026-06-13-welcome-to-the-lab.md", "topics:")
        self.assert_file_contains("topics.md", "post.topics")
        self.assert_file_contains("topics.md", "member.topics")
        self.assert_file_contains("topics.md", "all_topics")

    def test_member_issue_template_collects_profile_page_fields(self):
        self.assert_file_contains(".github/ISSUE_TEMPLATE/member-update.yml", "_members/")
        self.assert_file_contains(".github/ISSUE_TEMPLATE/member-update.yml", "slug")
        self.assert_file_contains(".github/ISSUE_TEMPLATE/member-update.yml", "研究主题")
        self.assert_file_contains(".github/ISSUE_TEMPLATE/member-update.yml", "个人页正文")

    def test_contribution_and_deployment_files_exist(self):
        for relative_path in [
            "CONTRIBUTING.md",
            "README.md",
            ".github/ISSUE_TEMPLATE/experience-post.yml",
            ".github/ISSUE_TEMPLATE/member-update.yml",
            ".github/workflows/pages.yml",
        ]:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), f"Missing file: {relative_path}")

    def test_pages_workflow_uses_jekyll_and_pages_actions(self):
        self.assert_file_contains(".github/workflows/pages.yml", "actions/jekyll-build-pages")
        self.assert_file_contains(".github/workflows/pages.yml", "actions/deploy-pages")

    def test_custom_domain_root_url_is_configured(self):
        self.assert_file_contains("_config.yml", 'url: "https://lgclab.github.io"')
        self.assert_file_contains("_config.yml", 'baseurl: ""')

    def test_homepage_has_polished_visual_structure(self):
        self.assert_file_contains("index.md", "hero-panel")
        self.assert_file_contains("assets/css/site.css", ".hero-panel")
        self.assert_file_contains("assets/css/site.css", ".section-grid")

    def test_homepage_does_not_depend_on_generated_images(self):
        self.assertFalse((ROOT / "assets/images/hero-network.png").exists())
        css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
        self.assertNotIn("hero-network", css)


if __name__ == "__main__":
    unittest.main()
