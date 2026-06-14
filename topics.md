---
title: "研究方向"
permalink: /topics/
---

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
{% assign all_topics = all_topics | uniq | sort %}

{% for topic in all_topics %}
  <section class="card">
    <h2>{{ topic }}</h2>

    <h3>相关经验贴</h3>
    <ul>
      {% assign has_posts = false %}
      {% for post in site.posts %}
        {% if post.topics contains topic %}
          {% assign has_posts = true %}
          <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a>{% if post.author %}，{{ post.author }}{% endif %}</li>
        {% endif %}
      {% endfor %}
      {% unless has_posts %}
        <li>暂无相关经验贴。</li>
      {% endunless %}
    </ul>

    <h3>相关成员</h3>
    <ul>
      {% assign has_members = false %}
      {% for member in site.members %}
        {% if member.topics contains topic %}
          {% assign has_members = true %}
          <li><a href="{{ member.url | relative_url }}">{{ member.name }}</a>{% if member.status %}，{{ member.status }}{% endif %}{% if member.open_to_contact %}，可联系{% endif %}</li>
        {% endif %}
      {% endfor %}
      {% unless has_members %}
        <li>暂无相关成员。</li>
      {% endunless %}
    </ul>
  </section>
{% else %}
  <p>还没有可汇总的主题。请在经验贴或成员页 front matter 中添加 topics 字段。</p>
{% endfor %}
