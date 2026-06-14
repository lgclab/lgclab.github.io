---
layout: default
title: "廖总全🌍后援会"
summary: "廖老板的研究生学生交流平台：沉淀经验，减少踩坑；连接同门，促进交流。"
kicker: "Research Group Knowledge & Connections"
---

<section class="hero-panel">
  <div class="hero-copy">
    <h1 class="hero-title">廖总全🌍后援会</h1>
    <p class="hero-summary">廖老板的研究生学生交流平台：沉淀经验，减少踩坑；连接同门，促进交流。</p>
    <div class="hero-actions">
      <a class="button" href="{{ '/posts/' | relative_url }}">看经验贴</a>
      <a class="button secondary" href="{{ '/members/' | relative_url }}">找成员</a>
    </div>
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

  {% assign all_topics = "" | split: "" %}
  {% for post in site.posts %}
    {% if post.topics %}
      {% assign all_topics = all_topics | concat: post.topics %}
    {% endif %}
  {% endfor %}
  {% for member in site.members %}
    {% if member.topics %}
      {% assign all_topics = all_topics | concat: member.topics %}
    {% endif %}
  {% endfor %}
  {% assign all_topics = all_topics | uniq %}
  {% assign topic_entries = "" | split: "" %}
  {% for topic in all_topics %}
    {% assign topic_content_count = 0 %}
    {% for post in site.posts %}
      {% if post.topics contains topic %}
        {% assign topic_content_count = topic_content_count | plus: 1 %}
      {% endif %}
    {% endfor %}
    {% for member in site.members %}
      {% if member.topics contains topic %}
        {% assign topic_content_count = topic_content_count | plus: 1 %}
      {% endif %}
    {% endfor %}
    {% if topic_content_count < 10 %}
      {% assign topic_sort_key = topic_content_count | prepend: "000" %}
    {% elsif topic_content_count < 100 %}
      {% assign topic_sort_key = topic_content_count | prepend: "00" %}
    {% elsif topic_content_count < 1000 %}
      {% assign topic_sort_key = topic_content_count | prepend: "0" %}
    {% else %}
      {% assign topic_sort_key = topic_content_count %}
    {% endif %}
    {% assign topic_entry = topic_sort_key | append: "||" | append: topic %}
    {% assign topic_entry_array = topic_entry | split: "^^" %}
    {% assign topic_entries = topic_entries | concat: topic_entry_array %}
  {% endfor %}
  {% assign topic_entries = topic_entries | sort | reverse %}

  <div class="section-grid">
    {% for topic_entry in topic_entries limit: 3 %}
      {% assign topic_parts = topic_entry | split: "||" %}
      {% assign topic = topic_parts | last %}
      {% assign topic_post_count = 0 %}
      {% assign topic_member_count = 0 %}
      {% for post in site.posts %}
        {% if post.topics contains topic %}
          {% assign topic_post_count = topic_post_count | plus: 1 %}
        {% endif %}
      {% endfor %}
      {% for member in site.members %}
        {% if member.topics contains topic %}
          {% assign topic_member_count = topic_member_count | plus: 1 %}
        {% endif %}
      {% endfor %}
      {% assign topic_content_count = topic_post_count | plus: topic_member_count %}
      <a class="card feature-card" href="{{ '/topics/' | relative_url }}">
        <span class="card-number">{% if forloop.index < 10 %}0{% endif %}{{ forloop.index }}</span>
        <h3>{{ topic }}</h3>
        <p>{{ topic_content_count }} 条相关内容：{{ topic_post_count }} 篇经验贴，{{ topic_member_count }} 位成员。</p>
      </a>
    {% else %}
      <a class="card feature-card" href="{{ '/topics/' | relative_url }}">
        <span class="card-number">01</span>
        <h3>暂无主题</h3>
        <p>在经验贴或成员页 front matter 中添加 topics 字段后，这里会自动显示最丰富的主题。</p>
      </a>
    {% endfor %}
  </div>
</section>

<section class="connection-band">
  <div>
    <p class="eyebrow">People Map</p>
    <h2>成员连接</h2>
  </div>
  <div class="connection-actions">
    <a class="button" href="{{ '/members/' | relative_url }}">查看成员</a>
    <a class="button secondary" href="{{ '/about/' | relative_url }}">了解维护规则</a>
  </div>
</section>
