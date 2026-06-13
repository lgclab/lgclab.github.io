---
layout: default
title: "课题组知识与连接站"
summary: "沉淀经验贴，帮助后来同学少走弯路；连接在组成员与毕业成员，让问题能找到合适的人。"
kicker: "Research Group Knowledge & Connections"
---

<section class="hero-panel">
  <div class="hero-copy">
    <p class="hero-kicker">Research Group Knowledge & Connections</p>
    <h1 class="hero-title">课题组知识与连接站</h1>
    <p class="hero-summary">沉淀经验贴，帮助后来同学少走弯路；连接在组成员与毕业成员，让问题能找到合适的人。</p>
    <div class="hero-actions">
      <a class="button" href="{{ '/posts/' | relative_url }}">看经验贴</a>
      <a class="button secondary" href="{{ '/members/' | relative_url }}">找成员</a>
    </div>
  </div>
</section>

<section class="metric-strip" aria-label="站点核心功能">
  <div class="metric">
    <strong>经验沉淀</strong>
    <span>入组、开题、论文、实验、毕业</span>
  </div>
  <div class="metric">
    <strong>成员连接</strong>
    <span>按方向、年级、可交流主题找人</span>
  </div>
  <div class="metric">
    <strong>低维护</strong>
    <span>Markdown 与 YAML 更新，GitHub Pages 自动发布</span>
  </div>
</section>

<section class="home-section">
  <div class="section-heading">
    <p class="eyebrow">Latest Notes</p>
    <h2>最近经验贴</h2>
  </div>

  <div class="list">
    {% for post in site.posts limit: 5 %}
      <a class="list-item featured-post" href="{{ post.url | relative_url }}">
        <div>
          <h3>{{ post.title }}</h3>
          <div class="meta-row">
            <span>{{ post.date | date: "%Y-%m-%d" }}</span>
            {% if post.author %}<span>{{ post.author }}</span>{% endif %}
            {% if post.category %}<span>{{ post.category }}</span>{% endif %}
          </div>
        </div>
        {% if post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 110 }}</p>{% endif %}
      </a>
    {% endfor %}
  </div>
</section>

<section class="home-section">
  <div class="section-heading">
    <p class="eyebrow">Browse</p>
    <h2>按主题进入</h2>
  </div>

  <div class="section-grid">
    <a class="card feature-card" href="{{ '/topics/' | relative_url }}">
      <span class="card-number">01</span>
      <h3>入组与科研启动</h3>
      <p>适合新同学快速了解组内工作方式、阅读节奏、开题准备和常见资源。</p>
    </a>
    <a class="card feature-card" href="{{ '/posts/' | relative_url }}">
      <span class="card-number">02</span>
      <h3>论文、实验与投稿</h3>
      <p>沉淀论文阅读、实验复现、写作修改、投稿 checklist 和会议经验。</p>
    </a>
    <a class="card feature-card" href="{{ '/members/' | relative_url }}">
      <span class="card-number">03</span>
      <h3>毕业、实习与去向</h3>
      <p>整理毕业流程、申博、找实习、求职和 alumni 可交流方向。</p>
    </a>
  </div>
</section>

<section class="connection-band">
  <div>
    <p class="eyebrow">People Map</p>
    <h2>成员连接</h2>
    <p>成员页不是通讯录，而是一个隐私友好的连接入口。每个人可以选择是否公开联系方式，并标注自己愿意交流的主题。</p>
  </div>
  <div class="connection-actions">
    <a class="button" href="{{ '/members/' | relative_url }}">查看成员</a>
    <a class="button secondary" href="{{ '/about/' | relative_url }}">了解维护规则</a>
  </div>
</section>
