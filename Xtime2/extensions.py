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

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()
avatars = Avatars() # 用户头像相关


@login_manager.user_loader
def load_user(user_id):
    # 创建用户加载回调函数，接受用户 ID 作为参数
    # 用 ID 作为 User 模型的主键查询对应的用户
    from Xtime2.models import User
    user = User.query.get(int(user_id))
    return user  # 返回用户对象
