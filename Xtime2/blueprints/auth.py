# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from Xtime2.extensions import db
from Xtime2.forms import LoginForm, RegisterForm
from Xtime2.models import Admin, User
from Xtime2.utils import redirect_back

"""
    auth模块负责用户登陆登出等权限问题
"""

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录用户使用 Flask-Login 提供的 login_user() 函数实现，需要传入用户模型类对象作为参数。
    :return:
    """
    # 用户已登录直接回到首页
    if current_user.is_authenticated:
        flash('用户已登录', 'info')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data   # bool类型，通过浏览器cookie实现记住登录的用户信息
        print(remember, type(remember))  # ...
        user = User.query.filter_by(username=username).first()
        if user:
            if user.validate_password(password):
                login_user(user, remember)
                flash('欢迎登录', 'success')
                return redirect_back()
            flash('用户名或密码错误', 'warning')
        else:
            flash('账户不存在.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    和登录相对，登出操作则需要调用 logout_user() 函数
    :return:
    """
    logout_user()
    flash('成功登出！', 'info')
    return redirect(url_for('auth.login'))
    # return redirect_back()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    print(1)
    # 已登录则重定向至main.index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        # 上面一句等价于if  request.method==' post '  and  from.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        confirm = form.confirm.data
        # 下面两句不需要调用，会自动调用
        # form.validate_username(form.username)
        # form.validate_email(form.email)

        # if form.validate_username(username) == True:
        #     flash('用户名已存在', 'warning')
        #     print('用户名已存在')
        # elif form.validate_email(email) == True:
        #     flash('邮箱已存在', 'warning')
        #     print('邮箱已存在')

        # 还需要验证合法性(用户名不能重复)
        user = User(
            name=name,
            email=email,
            username=username
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, None)  # 注册成功立即登录
        print('register success')
        return redirect_back()
    else:
        # 验证失败
        print('false')
        # return redirect(url_for('auth.register'))# 不能重定向到自己，应该会死循环
    return render_template('auth/register.html', form=form)
