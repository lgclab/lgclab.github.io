# 贡献指南

感谢为课题组知识与连接站补充内容。这个站点追求低维护、可持续、隐私友好。

## 新增经验贴

请在 `_posts/` 下新增 Markdown 文件，文件名格式为：

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
tags:
  - "新人"
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

## 更新成员信息

成员信息在 `_data/members.yml` 中维护。请只提交本人同意公开的信息。建议公开 GitHub、个人主页、Google Scholar、ORCID 或经过处理的邮箱，不建议公开手机号、微信号等敏感联系方式。

如果成员不想被直接联系，请设置：

```yaml
open_to_contact: false
```

## 更新研究方向

研究方向在 `_data/topics.yml` 中维护。每个方向可以关联经验贴和成员：

```yaml
related_posts:
  - "welcome-to-the-lab"
related_members:
  - "张三"
```

`related_posts` 使用文章 slug，一般来自 `_posts/YYYY-MM-DD-slug.md` 的 `slug` 部分。
