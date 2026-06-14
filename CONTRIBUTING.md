# 贡献指南

感谢为廖总全🌍后援会补充内容。这个站点追求低维护、可持续、隐私友好：普通同学可以通过 GitHub Issue 提交内容，熟悉 Git 的同学也可以直接提交 Pull Request。

## 通过 GitHub Issue 加入或发帖

这是推荐方式，适合大多数同学。

Issues 页面：[https://github.com/lgclab/lgclab.github.io/issues](https://github.com/lgclab/lgclab.github.io/issues)

### 新增或更新成员信息

1. 打开 Issues 页面。
2. 选择 **新增或更新成员** 模板。
3. 选择提交类型。新增成员时填写新 slug 和公开信息；更新成员时从下拉框选择已有 slug，只填写想修改的字段。
4. 勾选公开确认后提交。GitHub Actions 会自动写入或更新 `_members/` 下的成员页面。

成员信息请优先由本人提交。代为提交时，需要先确认对方同意公开哪些字段。建议公开 GitHub、个人主页、Google Scholar、ORCID 或经过处理的邮箱，不建议公开手机号、微信号等敏感联系方式。

如果 slug 已经被同名成员使用，系统会更新原页面；如果 slug 已经被不同姓名使用，系统会自动生成 `slug-2`、`slug-3`，避免覆盖他人页面。

更新成员时，留空字段会保留原成员页内容。

### 提交经验贴

1. 打开 Issues 页面。
2. 选择 **提交经验贴** 模板。
3. 填写标题、作者、自定义分类、多行 tags、适合读者和正文草稿。
4. 正文建议包含背景、具体做法、常见坑、推荐资源、后来者可以联系谁。

Issue 提交或编辑后，GitHub Actions 会把内容同步为网站中的 Markdown 文件。经验贴的分类和 tags 会自动写入 `topics`，所以会出现在主题页中。

## 通过 Pull Request 加入或发帖

如果你熟悉 GitHub，可以直接修改文件并提交 PR。

### 新增经验贴

在 `_posts/` 下新增 Markdown 文件，文件名格式为：

```text
YYYY-MM-DD-short-title.md
```

文章头部请保留以下信息：

```yaml
---
title: "文章标题"
author: "作者姓名"
date: 2026-06-13
category: "入组指南"
topics:
  - "入组指南"
  - "科研启动"
  - "论文阅读"
tags:
  - "科研启动"
  - "论文阅读"
audience: "新入组同学"
---
```

推荐正文结构：

```markdown
## 适合谁读

## 背景

## 具体做法

## 常见坑

## 推荐资源

## 后来者可以联系谁
```

### 新增或更新成员信息

成员信息在 `_members/` 中维护。每位成员一个 Markdown 文件，例如：

```text
_members/zhang-san.md
```

文件开头使用 front matter 保存可汇总的信息，正文可以写普通 Markdown：

```yaml
---
name: "张三"
title: "张三"
cohort: "2024"
role: "硕士"
status: "在组"
research:
  - "多智能体系统"
topics:
  - "多智能体系统"
  - "强化学习"
current: "课题组"
open_to_contact: true
contact_topics:
  - "入组前三个月怎么启动"
contact:
  github: "example-student"
  email: "name [at] example.com"
note: "请只填写本人同意公开的信息。"
---
```

如果成员不想被直接联系，请设置：

```yaml
open_to_contact: false
```

## 项目代码架构

这个项目是一个 GitHub Pages + Jekyll 静态站，不需要数据库或后台服务。

- `_config.yml`：站点标题、URL、集合、默认 layout 和发布排除项。
- `_layouts/`：页面、经验贴、成员页的 HTML 模板。
- `_posts/`：经验贴。每篇文章一个 Markdown 文件。
- `_members/`：成员页。每位成员一个 Markdown 文件。
- `index.md`：首页，包括最近经验贴、热门主题和成员连接入口。
- `posts.md`：经验贴列表页。
- `members.md`：成员列表页。
- `topics.md`：主题页，会自动汇总经验贴和成员页中的 `topics` 字段。
- `about.md`：网站目的和维护方式说明。
- `assets/css/site.css`：全站样式。
- `.github/ISSUE_TEMPLATE/`：成员信息和经验贴的 Issue 表单。
- `.github/workflows/issue-content-sync.yml`：Issue 创建或编辑后，自动生成或更新成员页和经验贴。
- `.github/workflows/pages.yml`：GitHub Pages 自动构建和发布流程。
- `scripts/sync_issue_content.py`：Issue 表单解析和 Markdown 生成逻辑。
- `scripts/update_member_issue_template.py`：从 `_members/*.md` 生成成员 Issue 表单里的已有 slug 下拉选项。
- `tests/`：轻量结构测试，防止关键页面、模板和字段被误删。

## 维护者应该做什么

普通同学只需要提交 Issue 或 PR；以下事项主要由维护者负责：

- 定期查看 Issue 同步是否成功；失败时检查 Actions 日志和 Issue 表单字段。
- 处理隐私边界，只公开提交者明确同意公开的字段。
- 检查自动生成的 front matter 是否完整，尤其是 `title`、`topics`、`open_to_contact` 等字段。
- 保持主题命名相对统一，避免同一个主题出现多个近义写法。
- 合并 PR 前运行结构测试：

```bash
python3 -m unittest
```

- 确认 `main` 分支合并后 GitHub Pages 正常发布。
- 如果修改网站结构，同步更新 README、贡献指南、Issue 模板和测试。
