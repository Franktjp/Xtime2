# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

# from Xtime2.blueprints.auth import admin_bp
from Xtime2.blueprints.auth import auth_bp
from Xtime2.blueprints.main import main_bp
from Xtime2.blueprints.user import user_bp
from Xtime2.extensions import bootstrap, db, login_manager, csrf, ckeditor, \
    mail, moment, toolbar, migrate
from Xtime2.models import Admin, User
from Xtime2.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        # 从环境变量读取FLASK_CONFIG的值，不存在则默认为development模式
        config_name = os.getenv('FLASK_CONFIG', 'development')

    # app = Flask(__name__)
    app = Flask('Xtime2')
    app.config.from_object(config[config_name]) # 从python对象中获取环境变量

    register_logging(app)       # 注册日志处理器
    register_extensions(app)    # 注册扩展(扩展初始化)
    register_blueprints(app)    # 注册蓝本
    register_commands(app)      # 注册自定义shell命令
    register_errors(app)        # 注册错误处理函数
    register_shell_content(app) # ...
    register_template_content(app)  # 注册模板上下文处理函数

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
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')


def register_shell_content(app):
    @app.shell_context_processor
    def make_shell_content():
        return dict(db=db)


def register_template_content(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400


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
        """Building Bluelog, just for you."""

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
        from Xtime2.fakes import fake_admin, fake_user

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        # fake_admin()
        fake_user()

        click.echo('Done.')
