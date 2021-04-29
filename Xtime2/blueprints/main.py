# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from Xtime2.forms import LoginForm
from Xtime2.models import Admin
from Xtime2.utils import redirect_back

"""
    main模块负责index等主要页面功能
"""

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')
