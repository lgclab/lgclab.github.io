---
title: "成员"
permalink: /members/
---

## 成员列表

<div class="member-list">
  {% assign members = site.members | sort: "cohort" | reverse %}
  {% for member in members %}
    <article class="member-card">
      <h3><a href="{{ member.url | relative_url }}">{{ member.name }}</a></h3>
      <div class="meta-row">
        {% if member.cohort %}<span>{{ member.cohort }} 级</span>{% endif %}
        {% if member.role %}<span>{{ member.role }}</span>{% endif %}
        {% if member.status %}<span>{{ member.status }}</span>{% endif %}
        {% if member.current %}<span>{{ member.current }}</span>{% endif %}
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
      <p><a href="{{ member.url | relative_url }}">查看个人页</a></p>
    </article>
  {% endfor %}
</div>
