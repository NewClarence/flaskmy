flask + mysql 搭建的注册登录项目
========
首次运行按照如下操作
--------
# 第一步，搭建虚拟开发环境<br>
virtualenv ./env<br>
# 第二步，安装依赖库<br>
source ./env/bin/active<br>
./env/bin/pip install -r requirements.txt<br>
# 第三步，创建数据库<br>
在config.py文件中修改成自己的mysql数据库<br>
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@hostname/database'<br>
然后执行<br>
./flask shell<br>
进入python的shell模式,执行<br>
db.create_all()<br>
Roles.insert_roles()<br>
# 第四步，启动<br>
./manage.py runserver -h 0.0.0.0<br>
