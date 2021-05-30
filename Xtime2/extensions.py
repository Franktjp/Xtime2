# -*- coding: utf-8 -*-

# 扩展类实例化

from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_avatars import Avatars
from flask_admin import Admin
from flask_babelex import Babel

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()
avatars = Avatars()     # 用户头像相关
admin = Admin(name='Xtime 后台管理系统')      # 后台管理
babel = Babel()         # 国际化


@login_manager.user_loader
def load_user(user_id):
    # 创建用户加载回调函数，接受用户 ID 作为参数
    # 用 ID 作为 User 模型的主键查询对应的用户
    """
    Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，如果\
    用户已登录， current_user 变量的值会是当前用户的用户模型类记录。
    :param user_id:
    :return:
    """
    from Xtime2.models import User
    user = User.query.get(int(user_id))
    return user  # 返回用户对象
