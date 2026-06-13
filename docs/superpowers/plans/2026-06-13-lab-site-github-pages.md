# Lab Site GitHub Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a low-maintenance GitHub Pages starter site for a research group with experience posts and member connection data.

**Architecture:** Use GitHub Pages with Jekyll so Markdown posts and YAML data files become a static website. Keep the first version small: homepage, posts index, members index, topics index, about page, layouts, shared CSS, contribution templates, and a Pages deployment workflow.

**Tech Stack:** GitHub Pages, Jekyll, Liquid templates, Markdown, YAML, GitHub Actions, Python unittest for repository structure checks.

---

### Task 1: Repository Structure Test

**Files:**
- Create: `tests/test_site_structure.py`

- [ ] **Step 1: Write failing structure tests**

Create a Python unittest that checks for the required Jekyll pages, data files, layouts, post template, workflow, and contribution docs.

- [ ] **Step 2: Run the test and verify it fails**

Run: `python3 -m unittest tests.test_site_structure`
Expected: fail because the site files do not exist yet.

### Task 2: Jekyll Site Scaffold

**Files:**
- Create: `_config.yml`
- Create: `index.md`
- Create: `posts.md`
- Create: `members.md`
- Create: `topics.md`
- Create: `about.md`
- Create: `_layouts/default.html`
- Create: `_layouts/page.html`
- Create: `_layouts/post.html`
- Create: `assets/css/site.css`

- [ ] **Step 1: Add the Jekyll config, pages, layouts, and CSS**

The site should expose the top-level navigation and render Markdown content, posts, members, and topics without a database.

### Task 3: Content Data and Templates

**Files:**
- Create: `_data/members.yml`
- Create: `_data/topics.yml`
- Create: `_posts/2026-06-13-welcome-to-the-lab.md`
- Create: `.github/ISSUE_TEMPLATE/experience-post.yml`
- Create: `.github/ISSUE_TEMPLATE/member-update.yml`
- Create: `CONTRIBUTING.md`
- Create: `README.md`

- [ ] **Step 1: Add starter data and contribution paths**

Provide sample member/topic data, one example post, issue templates for non-technical contributors, and concise contributor instructions.

### Task 4: GitHub Pages Deployment

**Files:**
- Create: `.github/workflows/pages.yml`

- [ ] **Step 1: Add Pages workflow**

Use the official Pages actions flow: checkout, configure Pages, build with Jekyll, upload artifact, deploy.

### Task 5: Verification

**Files:**
- Test: `tests/test_site_structure.py`

- [ ] **Step 1: Run structure tests**

Run: `python3 -m unittest tests.test_site_structure`
Expected: pass.

- [ ] **Step 2: Check repository status**

Run: `git status --short`
Expected: only intentional new files.
