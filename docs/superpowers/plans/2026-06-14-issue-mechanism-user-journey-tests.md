# Issue Mechanism User Journey Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Verify the GitHub Issue based content workflow from user intent through generated Markdown and site presentation for members and experience posts.

**Architecture:** Add user-journey tests that simulate GitHub issue form bodies, run `scripts/sync_issue_content.py` logic, and assert both generated content files and the site pages/layouts that surface that content. Any exposed behavior gaps are fixed in the sync script or documentation, not by adding explanatory website UI.

**Tech Stack:** Python `unittest`, Jekyll Markdown/Liquid source files, GitHub Issue Forms YAML.

---

### Task 1: Define User-Intent Test Matrix

**Files:**
- Create: `docs/issue-mechanism-test-log.md`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`

- [x] **Step 1: Document the intended journeys**

Record these journeys:

1. New member: user opens the `新增或更新成员` issue form, selects `新增成员`, fills name, slug, public fields, and submits. Target result: `_members/<slug>.md` exists, member appears on `/members/`, personal page `/members/<slug>/` contains profile body, topics page lists the member under each topic, and update dropdown includes the slug.
2. Update member: user opens the same form, selects `更新成员`, chooses an existing slug, fills only fields to change, and submits. Target result: the existing member file is updated, blank fields preserve previous values, personal page body updates when profile section fields are provided, and no duplicate page is created.
3. New experience post: user opens `提交经验贴`, fills title, author, custom category, tags, audience, and Markdown body. Target result: `_posts/YYYY-MM-DD-<slug>.md` exists, `/posts/` lists it, the post page shows metadata and body, and `/topics/` includes category and tags.
4. Update experience post: user edits the original issue for an existing post. Target result: the existing post file identified by `issue_number` is updated rather than creating a duplicate, and topic metadata reflects the edited category/tags.

- [x] **Step 2: Keep public-facing docs concise**

Add only durable mechanism notes to `README.md` and `CONTRIBUTING.md`, not site-visible explanatory headings.

### Task 2: Add Automated User Journey Tests

**Files:**
- Create: `tests/test_issue_user_journeys.py`

- [x] **Step 1: Write failing tests**

Add tests that create temporary repo roots, simulate issue bodies, run `sync_issue_content.sync_issue`, and assert generated files plus site source presentation paths.

- [x] **Step 2: Verify tests fail where behavior is incomplete**

Run:

```bash
python3 -m unittest tests.test_issue_user_journeys
```

Expected before fixes: failures should point to real gaps in the current mechanism or documentation.

### Task 3: Fix Exposed Gaps

**Files:**
- Modify only the minimal files required by failing tests.

- [x] **Step 1: Fix sync or docs behavior**

Address root causes surfaced by the tests.

- [x] **Step 2: Re-run focused tests**

Run:

```bash
python3 -m unittest tests.test_issue_user_journeys
```

Expected: all user-journey tests pass.

### Task 4: Full Verification

**Files:**
- No additional files unless verification exposes a gap.

- [x] **Step 1: Run all tests**

Run:

```bash
python3 -m unittest
```

Expected: all tests pass.

- [x] **Step 2: Run whitespace check**

Run:

```bash
git diff --check
```

Expected: no output and exit code 0.
