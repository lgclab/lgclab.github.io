---
title: "成员"
permalink: /members/
summary: "按成员状态、研究方向和可交流主题找到合适的人。公开联系方式默认遵循本人同意。"
---

## 当前成员

<div class="member-list">
  {% for member in site.data.members %}
    {% if member.status == "在组" %}
      <article class="member-card">
        <h3>{{ member.name }}</h3>
        <div class="meta-row">
          <span>{{ member.cohort }} 级</span>
          <span>{{ member.role }}</span>
          <span>{{ member.status }}</span>
        </div>
        {% if member.research %}
          <div class="tag-list">
            {% for item in member.research %}
              <span class="tag">{{ item }}</span>
            {% endfor %}
          </div>
        {% endif %}
        {% if member.note %}<p>{{ member.note }}</p>{% endif %}
        {% if member.open_to_contact %}
          <ul>
            {% for topic in member.contact_topics %}
              <li>{{ topic }}</li>
            {% endfor %}
          </ul>
          <p>
            {% if member.contact.github %}
              GitHub: <a href="https://github.com/{{ member.contact.github }}">{{ member.contact.github }}</a>
            {% elsif member.contact.email %}
              Email: {{ member.contact.email }}
            {% else %}
              可通过维护者转达联系请求。
            {% endif %}
          </p>
        {% endif %}
      </article>
    {% endif %}
  {% endfor %}
</div>

## 毕业成员

<div class="member-list">
  {% for member in site.data.members %}
    {% if member.status != "在组" %}
      <article class="member-card">
        <h3>{{ member.name }}</h3>
        <div class="meta-row">
          <span>{{ member.cohort }} 级</span>
          <span>{{ member.role }}</span>
          <span>{{ member.status }}</span>
        </div>
        {% if member.current %}<p>当前去向：{{ member.current }}</p>{% endif %}
        {% if member.research %}
          <div class="tag-list">
            {% for item in member.research %}
              <span class="tag">{{ item }}</span>
            {% endfor %}
          </div>
        {% endif %}
        {% if member.open_to_contact %}
          <ul>
            {% for topic in member.contact_topics %}
              <li>{{ topic }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      </article>
    {% endif %}
  {% endfor %}
</div>
