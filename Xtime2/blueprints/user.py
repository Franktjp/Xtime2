# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_required, current_user, logout_user, fresh_login_required

from Xtime2.extensions import db
from Xtime2.forms import LoginForm, RegisterForm, EditProfileForm
from Xtime2.models import Admin, User
# from Xtime2.utils import redirect_back

"""
    user模块负责用户设置(包括个人中心等等)
"""

user_bp = Blueprint('user', __name__)


@user_bp.route('/<username>', methods=['GET', 'POST'])
# 路由保护(需要登录才可访问)
@login_required
def profile(username):
    form = EditProfileForm()
    if request.method == 'POST':
        return redirect(url_for('user.edit_profile'))
    return render_template('user/profile.html', form=form)


@user_bp.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.gender = form.gender.data
        current_user.birthday = form.birthday.data
        current_user.signature = form.signature.data
        current_user.introduction = form.introduction.data
        db.session.commit()
        flash('个人资料已更新', 'success')
        return redirect(url_for('.profile', username=current_user.username))
    return render_template('user/settings/edit_profile.html', form=form)
