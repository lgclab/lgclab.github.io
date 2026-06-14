# 廖总全🌍后援会

廖总全🌍后援会是一个面向廖老板学生的交流平台。它希望把分散在不同届、不同方向、不同阶段里的经验沉淀下来，让后来同学少踩坑，也让在组成员和毕业成员更容易找到彼此。

## 网站包括什么

- **经验贴**：入组、开题、论文阅读、实验复现、投稿、毕业、实习、求职等真实经验。
- **成员信息**：在组成员和毕业成员的研究主题、可交流话题、当前状态和自愿公开的联系方式。
- **主题索引**：从经验贴和成员页里的 `topics` 自动汇总，帮助大家按主题找到资料和人。
- **维护说明**：说明网站如何收集内容、如何保护隐私、维护者如何更新网站。

## 如何加入或更新成员信息

成员信息主要通过 GitHub Issue 维护：

1. 打开 [Issues 页面](https://github.com/lgclab/lgclab.github.io/issues)。
2. 选择 **新增或更新成员** 模板。
3. 选择提交类型：新增成员时填写新 slug 和公开信息；更新成员时从下拉框选择已有 slug，只填写想修改的字段。
4. 提交或编辑 Issue 后，GitHub Actions 会自动同步到 `_members/` 下的成员页面。

成员信息请优先由本人提交。代为提交时，需要先确认对方同意公开哪些字段。不要提交手机号、微信号等敏感联系方式。

如果两个成员填写了相同 slug，但姓名不同，系统不会覆盖已有页面，会自动生成 `slug-2`、`slug-3` 这样的新页面。

更新成员时，留空字段会保留原成员页内容。

## 如何发布经验贴

经验贴也主要通过 GitHub Issue 维护：

1. 打开 [Issues 页面](https://github.com/lgclab/lgclab.github.io/issues)。
2. 选择 **提交经验贴** 模板。
3. 按模板填写标题、作者、自定义分类、多行 tags、适合读者和正文草稿。
4. 提交或编辑 Issue 后，GitHub Actions 会自动同步到 `_posts/` 下的 Markdown 文章。

经验贴的分类和 tags 会自动写入 `topics`，因此也会出现在主题页中。

如果你熟悉 GitHub，也可以直接提交 Pull Request。具体格式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 当前维护者

- **维护者**：Barytes
- **GitHub**：[@beiyanliu](https://github.com/beiyanliu)
- **维护范围**：处理自动同步异常、更新成员页和经验贴、维护网站结构、处理 GitHub Pages 发布。
- **联系维护者**：优先通过本仓库 [Issues](https://github.com/lgclab/lgclab.github.io/issues) 留言，方便后续追踪。

## 发布方式

本网站是 GitHub Pages 静态站。Issue 内容会先由 `.github/workflows/issue-content-sync.yml` 自动同步成 Markdown 文件；内容合并到 `main` 后，`.github/workflows/pages.yml` 会自动构建并发布新版网站。
