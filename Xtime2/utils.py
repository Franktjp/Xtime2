# -*- coding: utf-8 -*-

import os
import uuid

# try:
#     from urlparse import urlparse, urljoin
# except ImportError:
#     from urllib.parse import urlparse, urljoin
# # python3

from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app

from Xtime2.settings import BaseConfig  # 验证图片格式用到XTIME2_ALLOWED_IMAGE_EXTENSIONS


# 判断是否是安全的URL(不懂)
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='Xtime2.index', **kwargs):
# def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    """
    验证图片文件名格式正确性
    :param filename:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in BaseConfig.XTIME2_ALLOWED_IMAGE_EXTENSIONS


def rename_image(old_filename):
    """
    Generate a new_filename from the old_filename
    :param old_filename:
    :return:
    """
    # 将路径path拆分为一对，即(root, ext)，使root + ext == path，其中ext
    # 为空或以英文句点开头，且最多包含一个句点。路径前的句点将被忽略，例如splitext('.cshrc')返回('.cshrc', '')。
    # root = os.path.splitext(old_filename)[0]    # root
    ext = os.path.splitext(old_filename)[1]     # ext
    new_filename = uuid.uuid4().hex + ext       # such as 'e9b426dc9b4c4bfe8a637e29b9ff8a47' + ext
    # 注：uuid4根据随机数，或者伪随机数生成UUID，不保证唯一
    return new_filename



