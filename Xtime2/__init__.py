# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from Xtime2.blueprints.auth import auth_bp
from Xtime2.blueprints.main import main_bp
from Xtime2.blueprints.user import user_bp
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from Xtime2.extensions import bootstrap, db, login_manager, csrf, ckeditor, \
    mail, moment, toolbar, migrate, avatars, admin, babel
from Xtime2.models import Admin, Comment, Movie, movie_tag, Review, Tag, Topic, User
from Xtime2.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))       # {str} '....\\Pycharm\\Xtime2'
staticdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))


def create_app(config_name=None):
    if config_name is None:
        # 从环境变量读取FLASK_CONFIG的值，不存在则默认为development模式
        config_name = os.getenv('FLASK_CONFIG', 'development')

    # app = Flask(__name__)
    app = Flask('Xtime2')
    app.config.from_object(config[config_name]) # 从python对象中获取环境变量

    register_logging(app)           # 注册日志处理器
    register_extensions(app)        # 注册扩展(扩展初始化)
    register_blueprints(app)        # 注册蓝本
    register_commands(app)          # 注册自定义shell命令
    register_errors(app)            # 注册错误处理函数
    register_shell_content(app)     # ...
    register_template_context(app)  # 注册模板上下文处理函数

    return app


def register_logging(app):
    # 日志
    pass


def register_extensions(app):
    """
        导入所有扩展对象，并对其调用init_app()方法，传入程序实例完成初始化操作
    :param app:
    :return:
    """
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    """
        如果未登录的用户访问对应的 URL，Flask-Login 会把用户重定向到登录页面，并显示一个错误提示。
        为了让这个重定向操作正确执行，我们还需要把 login_manager.login_view 的值设为我们程序的登录视图端点（函数名）
        把代码`login_manager.login_view = 'auth.login'`放到 login_manager 实例定义下面即可
        
        提示:如果你需要的话，可以通过设置 login_manager.login_message 来自定义错误提示消息。

        参考：[Flask 第 8 章：用户认证视图保护部分](https://read.helloflask.com/c8-login)
    """
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app)
    avatars.init_app(app)
    admin.init_app(app)
    babel.init_app(app)

    # 以下为Xtime 后台管理系统增加数据库模型视图
    admin.add_view(ModelView(Admin, db.session, endpoint='admin_admin', name='管理员'))
    admin.add_view(ModelView(Comment, db.session, endpoint='comment_admin', name='评论'))
    admin.add_view(ModelView(Movie, db.session, endpoint='movie_admin', name='影片'))
    # admin.add_view(ModelView(movie_tag, db.session, endpoint='movie_tag_admin', name=''))  # error: AttributeError: 'Table' object has no attribute '__name__'
    admin.add_view(ModelView(Review, db.session, endpoint='review_admin', name='影评'))
    admin.add_view(ModelView(Tag, db.session, endpoint='tag_admin', name='标签'))
    admin.add_view(ModelView(Topic, db.session, endpoint='topic_admin', name='话题'))
    admin.add_view(ModelView(User, db.session, endpoint='user_admin', name='用户'))
    # admin.add_view(FileAdmin(os.path.join(basedir, 'uploads'), '/static/', name='文件'))
    # 设置文件管理文件夹为static，但是这么做好像很危险。仅作尝试，应用程序文件管理应该更加专业
    admin.add_view(FileAdmin(staticdir, '/static/', name='文件'))


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    # app.register_blueprint(admin_bp)


def register_shell_content(app):
    @app.shell_context_processor
    def make_shell_content():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    # 模板上下文处理函数
    def make_template_context():
        user = current_user
        # if current_user.is_authenticated:
        #     notification_count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
        # else:
        #     notification_count = None
        # return dict(notification_count=notification_count)
        # 注：瞎写的，因为只要函数定义就不能pass，具体见模板上下文处理函数 or https://read.helloflask.com/c6-template2
        return dict(user=user)


def register_errors(app):
    @app.errorhandler(400)  # 传入要处理的错误代码
    def bad_request(e):     # 接受异常对象作为参数
        return render_template('errors/400.html'), 400  # 返回模板和状态码

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404  # 返回模板和状态码


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        """Initialize the database"""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """
            创建管理员账户，执行`flask init`命令创建账户
        """

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                name='Admin'
            )
            admin.set_password(password)
            db.session.add(admin)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    def forge():
        """Generate fake data."""
        from Xtime2.fakes import fake_admin, fake_user, fake_movie, fake_review

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        # fake_admin()
        fake_user()
        fake_movie()
        fake_review()

        click.echo('Done.')
