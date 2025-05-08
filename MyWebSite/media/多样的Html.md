# 在app目录下创建这样的结构

```plaintext
myapp/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   └── myapp/
│       └── index.html
```

# 在html文件中使用js和css文件资源时

```
使用 {% load static %}一次即可
```

# 在主项目目录下

```python
# settings.py
import os

# 静态文件的 URL 前缀
STATIC_URL = '/static/'

# 项目根目录下的静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 收集静态文件后的存放目录
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

# 在跳转链接中使用

该文件中的name

```python
# login/urls.py
from django.urls import path
from .views import register_view  # 假设你的注册视图名为 register_view

urlpatterns = [
    # 原硬编码路径：127.0.0.1:8000/display/
    # 改为命名 URL，路径和名称可灵活修改
    path('register/', register_view, name='register'),  # 推荐路径用有意义的名称，如 'register/'
]
```

```python
<p class="signup-link">
  没有账号？<a href="{% url 'register' %}">立即注册</a>  <!-- 关键修改：使用 {% url 'register' %} -->
</p>
```





```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 加载静态文件标签 -->
    {% load static %}
    <!-- 引入 CSS 文件 -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <title>My Page</title>
</head>
<body>
    <h1>Welcome to my page</h1>
    <!-- 引入 JS 文件 -->
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

