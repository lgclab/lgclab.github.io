import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteStructureTest(unittest.TestCase):
    def assert_file_contains(self, relative_path, expected_text):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"Missing file: {relative_path}")
        content = path.read_text(encoding="utf-8")
        self.assertIn(expected_text, content, f"{relative_path} should contain {expected_text!r}")

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
        self.assert_file_contains("members.md", "site.data.members")
        self.assert_file_contains("topics.md", "site.data.topics")
        self.assert_file_contains("about.md", "如何参与维护")

    def test_layouts_and_styles_exist(self):
        for relative_path in [
            "_layouts/default.html",
            "_layouts/page.html",
            "_layouts/post.html",
            "assets/css/site.css",
        ]:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), f"Missing file: {relative_path}")

    def test_data_files_have_connection_fields(self):
        self.assert_file_contains("_data/members.yml", "open_to_contact")
        self.assert_file_contains("_data/members.yml", "contact_topics")
        self.assert_file_contains("_data/topics.yml", "related_posts")
        self.assert_file_contains("_data/topics.yml", "related_members")

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

    def test_project_pages_baseurl_is_configured(self):
        self.assert_file_contains("_config.yml", 'baseurl: "/lab-site"')

    def test_homepage_has_polished_visual_structure(self):
        self.assert_file_contains("index.md", "hero-panel")
        self.assert_file_contains("index.md", "metric-strip")
        self.assert_file_contains("assets/css/site.css", ".hero-panel")
        self.assert_file_contains("assets/css/site.css", ".metric-strip")

    def test_homepage_does_not_depend_on_generated_images(self):
        self.assertFalse((ROOT / "assets/images/hero-network.png").exists())
        css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
        self.assertNotIn("hero-network", css)


if __name__ == "__main__":
    unittest.main()
