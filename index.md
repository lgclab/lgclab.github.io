---
title: "课题组知识与连接站"
summary: "沉淀经验贴，帮助后来同学少走弯路；连接在组成员与毕业成员，让问题能找到合适的人。"
kicker: "Research Group Knowledge & Connections"
---

<div class="hero-actions">
  <a class="button" href="{{ '/posts/' | relative_url }}">看经验贴</a>
  <a class="button secondary" href="{{ '/members/' | relative_url }}">找成员</a>
</div>

## 最近经验贴

<div class="list">
  {% for post in site.posts limit: 5 %}
    <a class="list-item" href="{{ post.url | relative_url }}">
      <h3>{{ post.title }}</h3>
      <div class="meta-row">
        <span>{{ post.date | date: "%Y-%m-%d" }}</span>
        {% if post.author %}<span>{{ post.author }}</span>{% endif %}
        {% if post.category %}<span>{{ post.category }}</span>{% endif %}
      </div>
      {% if post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 96 }}</p>{% endif %}
    </a>
  {% endfor %}
</div>

## 按主题进入

<div class="section-grid">
  <section class="card">
    <h3>入组与科研启动</h3>
    <p>适合新同学快速了解组内工作方式、阅读节奏、开题准备和常见资源。</p>
  </section>
  <section class="card">
    <h3>论文、实验与投稿</h3>
    <p>沉淀论文阅读、实验复现、写作修改、投稿 checklist 和会议经验。</p>
  </section>
  <section class="card">
    <h3>毕业、实习与去向</h3>
    <p>整理毕业流程、申博、找实习、求职和 alumni 可交流方向。</p>
  </section>
</div>

## 成员连接

<div class="section-grid">
  <section class="card">
    <h3>当前成员</h3>
    <p>了解组里有哪些同学、各自在做什么方向、可以交流哪些主题。</p>
  </section>
  <section class="card">
    <h3>毕业成员</h3>
    <p>保留师兄师姐的去向和可联系主题，帮助后来的同学找到合适的人。</p>
  </section>
  <section class="card">
    <h3>隐私优先</h3>
    <p>公开展示的联系方式默认需要本人同意，敏感信息不放在网站上。</p>
  </section>
</div>
