# 创建项目：

```
django-admin startproject 【HelloWorld】
```



# 启动服务器（需要在项目文件夹路径下）：

```
python manage.py runserver
```



# 创建一个新的APP：

```
 django-admin startapp 【test】
```



# 创建一个新的APP时，需要在主项目目录下的setting.py文件下修改INSTALLED_APPS，添加新APP的名称

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'test',
]
```



# 在APP目录下，编写view代码

```python
from django.shortcuts import render
# Create your views here.
def hello(request):
    return render(request, template_name="hello.html" , context={'message':'hello_world'})
	#			要求						模板文件			内容
```



# 在APP目录下，创建模板文件夹（templates）：

创建文件**hello.html**

{{ message }}模板中的变量传递

```html
<html>
    <head>
        <meta charset="UTF-8">
        <title>Title</Title>

    </head>
    <body>
        <h1> {{message}} </h1>
    </body>
</html>
```



# 修改主项目目录下的urls.py文件

```python
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('test.urls'))
]
```



# 在APP目录下创建urls.py文件

```python
from django.urls import path
from .views import hello
urlpatterns = [
    path('hello/',hello,name='hello'),
	# 访’问hello/‘的时候，调用当前app目录下，views文件中的hello函数
]

```



# 数据库配置

```python
# 我们在项目的 settings.py 文件中找到 DATABASES 配置项
DATABASES = { 
    'default': 
    { 
        'ENGINE': 'django.db.backends.mysql',    # 数据库引擎
        'NAME': 'runoob', # 数据库名称
        'HOST': '127.0.0.1', # 数据库地址，本机 ip 地址 127.0.0.1 
        'PORT': 3306, # 端口 
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456', # 数据库密码
    }  
}
```

在项目主目____init____.py下添加：

```python
import pymysql
pymysql.install_as_MySQLdb()
```



# 创建模型：

在APP目录下的models.py文件中写入ORM（对象关系映射），设计好数据表结构



# 生成迁移文件：

要在主项目录下的终端执行

```bash
python manage.py makemigrations
```

# 将迁移文件应用到数据库：

```bash
python manage.py migrate
```

# 创建一个后台管理用户

```
python manage.py createsuperuser
```

# 进入默认的后台管理

127.0.0.1:8000/admin

# 注册模型

进入到app目录中的admin.py下

```python
from django.contrib import admin
from .models import Author ,Article 
# Author ,Article 根据注册模型的名称改变

# Register your models here.
admin.site.register(Author)
admin.site.register(Article)
```

# 设置中文界面

进入到主项目目录中的setting.py文件下

找到LANGUAGE_CODE并修改为'zh-hans'

```
LANGUAGE_CODE = 'zh-hans'
```

