# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, send_from_directory, \
    current_app, request
from flask_login import login_user, logout_user, login_required, current_user

from Xtime2.extensions import db
from Xtime2.forms import LoginForm
from Xtime2.models import Admin, Movie, Tag
from Xtime2.utils import redirect_back

"""
    main模块负责index等主要页面功能
"""

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('main/index.html')
    # movies数据,应该从数据库中获取
    # 我只需要影片的id、封面图、name、评分
    movies = Movie.query.order_by(Movie.score.desc()).limit(6).all()
    movies_dict = []
    for movie in movies:
        m_dict = {
            'id': movie.id,
            'thumbnail': movie.image,
            'title': movie.name,  # 需要注意的是有中文字符的要不要加u
            'rating': movie.score
        }
        movies_dict.append(m_dict)

    # return render_template('main/test.html', cards=movies)
    # return render_template('main/index.html', cards=movies)
    return render_template('main/index.html', cards=movies_dict)


@main_bp.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    tags = movie.tags.all() # 获取该影片所有的tag
    # print('tag: ', tags)
    movie_dict = {
        'id': movie.id,
        'name': movie.name,
        'image': movie.image,
        'desc': movie.desc,
        'release_date': movie.release_date,
        'mins': movie.mins,
        'score': movie.score,
        # 'tags': []
        'tags': movie.tags
    }
    # 关于如何显示所有的tag，一是后端将tags列表中的tag.name拿出来放进新的列表中
    # 二是直接由前端的模板语句将tags中的tag.name拿出来。采用第二种方式
    # for tag in tags:
    #     # tags是一个列表，存放n各Tag对象。tag是一个Tag对象
    #     movie_dict['tags'].append(tag.name)
    return render_template('main/movie_index.html', movie=movie_dict)


@main_bp.route('/movie/<int:movie_id>/desc', methods=['GET', 'POST'])
def get_movie_desc(movie_id):
    movie = Movie.query.get(movie_id)
    tags = movie.tags.all() # 获取该影片所有的tag
    movie_dict = {
        'id': movie.id,
        'name': movie.name,
        'image': movie.image,
        'desc': movie.desc,
        'release_date': movie.release_date,
        'mins': movie.mins,
        'score': movie.score,
        # 'tags': []
        'tags': movie.tags
    }
    return render_template('main/movie_desc.html', movie=movie_dict)


@main_bp.route('/movie/<int:movie_id>/more', methods=['GET', 'POST'])
def get_movie_more(movie_id):
    movie = Movie.query.get(movie_id)
    tags = movie.tags.all() # 获取该影片所有的tag
    movie_dict = {
        'id': movie.id,
        'name': movie.name,
        'image': movie.image,
        'desc': movie.desc,
        'release_date': movie.release_date,
        'mins': movie.mins,
        'score': movie.score,
        # 'tags': []
        'tags': movie.tags
    }
    return render_template('main/movie_more.html', movie=movie_dict)


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@main_bp.route('/list')
def item_list():
    # category = int(request.args.get('category'))
    items = None
    # if category == 1:
    #     items = movies
    # else:
    #     items = tvs
    return render_template('index.html', items=items)

