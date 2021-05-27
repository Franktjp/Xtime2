# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, send_from_directory, \
    current_app, request, json
from flask_login import login_user, logout_user, login_required, current_user

from Xtime2.extensions import db
from Xtime2.forms import LoginForm, ReviewForm, CommentForm
from Xtime2.models import Admin, User, Movie, Tag, Review, Comment
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
    return render_template('main/movie_index.html', movie=movie_dict, )


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


# ...
@main_bp.route('/<int:movie_id>/review/new', methods=['GET', 'POST'])
@login_required
def create_review(movie_id):
    form = ReviewForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        movie = Movie.query.get(movie_id)
        review = Review(title=title, content=content, user_id=user_id, movie_id=movie_id)
        db.session.add(review)
        db.session.commit()
        flash("影评发表成功", "success")
        # return redirect(url_for('main.index', review_id=review.id))
        return redirect(url_for('main.show_review', review_id=review.id))
    movie = Movie.query.get(movie_id)
    context = {
        'form': form,
        'movie': movie
    }
    # ** context    参考：[flask--渲染Jinja模板与传入模板变量](https://blog.csdn.net/xujin0/article/details/95972917)
    return render_template('main/review_create.html', **context)


@main_bp.route('/review/<int:review_id>', methods=['GET', 'POST'])
def show_review(review_id):
    review = Review.query.get_or_404(review_id)
    # page = request.args.get('page', 1, type=int)
    # per_page = current_app.config['XTIME_COMMENT_PER_PAGE']
    # pagination = Comment.query.with_parent(review).filter_by(checked=True).order_by(Comment.timestamp.asc()).paginate(
    #     page, per_page
    # )
    # comments = pagination.items

    form = CommentForm()
    # 用户已登录和游客均可以评论，游客用户名显示游客
    if current_user.is_authenticated:
        checked = True
    else:
        checked = False

    if form.validate_on_submit():
        content = form.content.data
        comment = Comment(
            content=content,
            # review = review,
            checked=checked)

    user = User.query.get_or_404(review.user_id)
    movie = Movie.query.get_or_404(review.movie_id)
    context = {
        'review': review,
        'movie': movie,
        'user': user
    }
    return render_template('main/review_show.html', **context)


@main_bp.route('/review/<int:review_id>/praise', methods=['GET', 'POST'])
@login_required
def praise_review(review_id):
    try:
        review_id = request.form['review_id']
        checked = request.form['checked']
        review = Review.query.get(review_id)
        movie = review.movie
        user = review.user
        context = {
            'review': review,
            'movie': movie,
            'user': user
        }
        # 用户未登录，直接返回影评详情页面
        if not current_user.is_authenticated:
            flash('用户未登录', 'warning')
            return render_template('main/review_show.html', **context)
        # 通过主键未查询到该影评
        if not review_id:
            if checked:
                return json.dumps({
                    'status': '点赞失败',
                    'fav_nums': review.fav_nums
                })
            else:
                return json.dumps({
                    'status': '取消点赞失败',
                    'fav_nums': review.fav_nums
                })
        # 注意返回的checked是str类型，而且js中是小写true/false，而不是bool类型
        if checked == 'false' or checked == 'False':
            review.fav_nums = review.fav_nums - 1
        else:
            review.fav_nums = review.fav_nums + 1
        db.session.commit()

        # if checked:
        #     flash('点赞成功', 'success')
        # else:
        #     flash('取消点赞成功', 'success')
        return json.dumps({
            'status': 'OK',
            'fav_nums': review.fav_nums
        })
    except Exception as e:
        print(e)
        return render_template('error.html', error=str(e))
    # 下面语句执行不到，考虑重新刷新点赞数，用jQuery解决
    # return render_template('main/review_show.html', **context)


@main_bp.route('/review/<int:review_id>/step', methods=['GET', 'POST'])
@login_required
def step_review(review_id):
    pass

