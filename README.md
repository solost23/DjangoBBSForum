# DjangoBBSForum
基于python3.7 + Django2.2.4 + Mysql5.7 实现的BBS论坛
## 主要功能
- 实现不同的论坛板块
- 帖子列表展示
- 帖子评论数、点赞数展示
- 在线用户展示
- 允许登录用户发帖、评论、点赞
- 允许上传文件
- 帖子可被置顶显示
- 可进行多级评论（实现评论树）
## 安装
### 下载
    git clone git@github.com:Solost23/DjangoBBSForum.git
### 依赖环境安装
    pip install -r requirements.txt
### 配置
配置都是在settings.py中。
## 运行
修改DjangoBBSForum/settings.py修改数据库配置，如下所示：

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bbs',
            'USER': 'Username',
            'PASSWORD': 'Password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

### 创建数据库
这里为了省去本机安装mysql等繁琐的步骤，采用docker搭建数据库环境。

    docker run --name oneMysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123 -d mysql:5.7

CMD中进入 oneMysql容器，然后在终端执行命令进入 mysql 并创建一个数据库bbs
    
    docker exec -it oneMysql bash
    CREATE DATABASE bbs CHARACTER SET utf8;
    
然后终端下执行：

    ./python manage.py makemigrations
    ./python manage.py migrate
    
### 创建超级用户（进入admin的时候需要）
终端下执行：

    ./python manage.py createsuperuser
    
### 开始运行
    ./python manage.py runserver 0.0.0.0:8000
    
浏览器打开：http://127.0.0.1:8000/ 就可以看到效果了，http://127.0.0.1:8000/admin/ 可访问网站后台，用户名和密码为超级用户的用户名和密码。


