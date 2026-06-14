# Issue Mechanism Test Log

Date: 2026-06-14

This document records the intended GitHub Issue workflows for maintainers. It is excluded from GitHub Pages publishing in `_config.yml`.

## Test Matrix

| User intent | User action | Target result | Automated coverage |
| --- | --- | --- | --- |
| 新增成员 | Open the `新增或更新成员` issue form, choose `新增成员`, fill slug, public profile fields, contact fields, topics, and consent. | A new `_members/<slug>.md` file is generated. `/members/` can list the member. `/members/<slug>/` can render profile body and public contact. `/topics/` can show the member under each topic. The member update dropdown includes the new slug. | `tests/test_issue_user_journeys.py::test_user_can_add_member_and_site_can_surface_member_everywhere` |
| 更新成员 | Open the same issue form, choose `更新成员`, select an existing slug, and fill only fields to change. | The existing member Markdown file is updated in place. Blank fields preserve prior values. No duplicate member page is created. Profile section fields update the personal page body. | `tests/test_issue_user_journeys.py::test_user_can_update_existing_member_without_creating_duplicate` |
| 新增经验贴 | Open the `提交经验贴` issue form, fill title, author, custom category, tags, audience, and Markdown body. | A new `_posts/YYYY-MM-DD-<slug>.md` file is generated. `/posts/` can list it. The post page can render metadata, tags, and body. `/topics/` can show category and tags. | `tests/test_issue_user_journeys.py::test_user_can_add_experience_post_and_site_can_surface_post_everywhere` |
| 更新经验贴 | Edit the original experience-post issue. | The original post file is updated by `issue_number`. No duplicate article is created. Category and tags are replaced by the edited values. | `tests/test_issue_user_journeys.py::test_user_can_update_existing_experience_post_by_editing_original_issue` |

## Findings And Fixes

- Public contact parsing already accepted `GitHub`, `Email`, `Homepage`, `Scholar`, and `ORCID`, but the member list and member profile layout only displayed GitHub or Email. The layouts now render all supported public contact fields.
- README and CONTRIBUTING did not describe the newer member profile section fields. They now describe `我在做什么`, `可交流主题`, `个人经验`, and the full Markdown override field.
- README and CONTRIBUTING now state that editing the original experience-post issue updates the existing article through `issue_number`.
