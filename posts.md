---
title: "经验贴"
permalink: /posts/
summary: "一篇文章解决一个具体问题：入组、开题、论文、实验、投稿、毕业、实习和求职。"
---

<div class="list">
  {% for post in site.posts %}
    <a class="list-item" href="{{ post.url | relative_url }}">
      <h3>{{ post.title }}</h3>
      <div class="meta-row">
        <span>{{ post.date | date: "%Y-%m-%d" }}</span>
        {% if post.author %}<span>{{ post.author }}</span>{% endif %}
        {% if post.category %}<span>{{ post.category }}</span>{% endif %}
        {% if post.audience %}<span>{{ post.audience }}</span>{% endif %}
      </div>
      {% if post.tags %}
        <div class="tag-list">
          {% for tag in post.tags %}
            <span class="tag">{{ tag }}</span>
          {% endfor %}
        </div>
      {% endif %}
      {% if post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 140 }}</p>{% endif %}
    </a>
  {% endfor %}
</div>

<div class="inline-actions">
  <a class="button secondary" href="{{ '/about/' | relative_url }}">查看投稿方式</a>
</div>
