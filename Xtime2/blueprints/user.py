# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_required, current_user, logout_user, fresh_login_required

from Xtime2.extensions import db, avatars
from Xtime2.forms import LoginForm, RegisterForm, EditProfileForm, UploadAvatorForm, CropAvatorForm
from Xtime2.models import Admin, User

# from Xtime2.utils import allowed_file, rename_image

# from Xtime2.settings import basedir, BaseConfig # 用到 工程路径basedir 和 文件存储路径XTIME2_UPLOAD_PATH


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
        if current_user.gender == 'M':  # 男
            current_user.gender = 1
        if current_user.gender == 'F':  # 女
            current_user.gender = 2
        if current_user.gender == 'N':  # 其他
            current_user.gender = None
        db.session.commit()
        flash('个人资料已更新', 'success')
        return redirect(url_for('.profile', username=current_user.username))
    return render_template('user/settings/edit_profile.html', form=form)


@user_bp.route('/settings/avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    upload_form = UploadAvatorForm()
    crop_form = CropAvatorForm()
    return render_template('user/settings/change_avatar.html', upload_form=upload_form, crop_form=crop_form)


@user_bp.route('/settings/avatar/upload', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    form = UploadAvatorForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = avatars.save_avatar(photo)   # 注：此种方式上传图片需要app实例配置AVATARS_SAVE_PATH选项
        current_user.avatar_raw = filename
        db.session.commit()
        flash('上传头像成功', 'success')
    return redirect(url_for('.change_avatar'))


@user_bp.route('/settings/avatar/crop', methods=['GET', 'POST'])
@login_required
def crop_avatar():
    form = CropAvatorForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        w = form.w.data
        h = form.h.data
        filenames = avatars.crop_avatar(current_user.avatar_raw, x, y, w, h)
        current_user.avatar_s = filenames[0]
        current_user.avatar_m = filenames[1]
        current_user.avatar_l = filenames[2]
        db.session.commit()
        flash('头像更新成功', 'success')

    return redirect(url_for('.change_avatar'))
