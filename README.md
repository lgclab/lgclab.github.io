# 课题组知识与连接站

这是一个面向课题组的 GitHub Pages 静态网站，用来沉淀经验贴并维护成员连接入口。

## 核心板块

- `经验贴`：入组、开题、论文、实验、投稿、毕业、实习和求职经验。
- `成员`：当前成员、毕业成员、研究方向、可交流主题和自愿公开的联系方式。
- `研究方向`：按研究问题连接相关经验贴和成员。
- `关于课题组`：说明网站目的、内容边界和维护方式。

## 常见维护

新增经验贴：在 `_posts/` 中新增 `YYYY-MM-DD-title.md` 文件，并填写 front matter。

更新成员：编辑 `_data/members.yml`。

更新研究方向：编辑 `_data/topics.yml`。

## 发布

仓库启用 GitHub Pages 后，`.github/workflows/pages.yml` 会在推送到 `main` 时自动构建并发布。

在 GitHub 仓库设置中进入 `Settings -> Pages`，将 `Build and deployment` 的 `Source` 设置为 `GitHub Actions`。
