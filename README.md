# DjangoBBSForum
基于`python3.7` + `Django3.2` + `mysql5.7` + `CKEditor 5 Classic`实现的前后端不分离BBS论坛
## 主要功能
#### BBS主要功能
- 实现不同的论坛板块（前端展示板块可动态变化）
- 帖子列表展示
- 帖子评论数、点赞数展示
- 在线用户展示
- 允许登录用户发帖、评论、点赞
- 允许上传文件
- 帖子可被置顶显示
- 可进行多级评论（实现评论树、动态加载评论等）
- 页面新消息自动提醒
- **用户注册登录功能待优化**
## 安装
### 下载
```bash
git clone git@github.com:Solost23/DjangoBBSForum.git
```
    
### 依赖环境安装
```bash
pip install -r requirements.txt
```
    
### 配置
配置都在 `DjangoBBSForum/settings.py` 中。
## 运行
修改 `DjangoBBSForum/settings.py` 修改数据库配置，如下所示：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bbs',
        'USER': 'root',
        'PASSWORD': 'Password',
        'HOST': 'host',
        'PORT': '3306',
    }
}
```
    
### 创建数据库
这里为了省去本机安装 `mysql` 等繁琐的步骤，采用 `docker` 搭建数据库环境。
```bash
docker run --name oneMysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123 -d mysql:5.7
```
    
CMD中进入 `oneMysql` 容器，然后在终端执行命令进入 `mysql` 并创建一个数据库 `bbs`
```bash
docker exec -it oneMysql bash
CREATE DATABASE bbs CHARACTER SET utf8;
```

然后终端下执行：
```bash
./manage.py makemigrations
./manage.py migrate
```
 
**注意：** 在使用 `./manage.py` 之前需要确定你系统中的 `python` 命令是指向 `python3.6` 及以上版本的（3.6版本及以上执行.py文件的时候不加 `python` 也可以）。如果不是如此，请使用以下两种方式中的一种：
- 修改 `manage.py` 第一行 `#!/usr/bin/env python` 为 `#!/usr/bin/env python3`
- 直接使用 `python ./manage.py makemigrations` 
    
### 创建超级用户（进入admin的时候需要）
终端下执行：
```bash
./manage.py createsuperuser
```

### 开始运行
```bash
./manage.py runserver 0.0.0.0:8000
```
    
- 浏览器打开：http://127.0.0.1:8000/bbs/ 就可以看到 BBS 效果了
- 浏览器打开：http://127.0.0.1:8000/admin/ 可访问网站后台，用户名和密码为超级用户的用户名和密码


