---
title: "研究方向"
permalink: /topics/
summary: "从研究问题进入资料和人：每个方向都连接相关经验贴、当前成员和可联系的毕业成员。"
---

{% for topic in site.data.topics %}
  <section class="card">
    <h2>{{ topic.name }}</h2>
    <p>{{ topic.description }}</p>

    {% if topic.keywords %}
      <div class="tag-list">
        {% for keyword in topic.keywords %}
          <span class="tag">{{ keyword }}</span>
        {% endfor %}
      </div>
    {% endif %}

    {% if topic.related_posts %}
      <h3>相关经验贴</h3>
      <ul>
        {% for post in site.posts %}
          {% if topic.related_posts contains post.slug %}
            <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
          {% endif %}
        {% endfor %}
      </ul>
    {% endif %}

    {% if topic.related_members %}
      <h3>可交流成员</h3>
      <ul>
        {% for member in site.data.members %}
          {% if topic.related_members contains member.name %}
            <li>{{ member.name }}{% if member.status %}，{{ member.status }}{% endif %}{% if member.open_to_contact %}，可联系{% endif %}</li>
          {% endif %}
        {% endfor %}
      </ul>
    {% endif %}
  </section>
{% endfor %}
