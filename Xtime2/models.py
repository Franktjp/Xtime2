# -*- coding: utf-8 -*-

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from Xtime2.extensions import db


class Admin(db.Model, UserMixin):
    """
        管理员模型
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    # blog_title = db.Column(db.String(60))
    # blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(db.Model, UserMixin):
    """
    普通用户实体：姓名、用户名(username)/昵称(nickname)、密码、手机号、邮箱、性别、生日、地址、个性签名(比如知乎的一句话介绍)、
               个人介绍、头像、用户权限(该字段可以不考虑，管理员应该与普通用户独立)
    """
    # 创建数据库模型
    id = db.Column(db.Integer, primary_key=True)  # ID
    name = db.Column(db.String(20))  # 姓名
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值
    phone = db.Column(db.String(13))  # 手机号
    email = db.Column(db.String(30))  # email
    # email = db.Column(db.String, nullable=True, unique=True)

    gender = db.Column(db.Integer, default=None)  # 性别(默认为空)
    birthday = db.Column(db.Date)  # 出生日期
    # address = None                                  # 地址(暂时不用)
    signature = db.Column(db.String(50))  # 个性签名(比如知乎的一句话介绍)
    introduction = db.Column(db.Text)  # 个人介绍
    # 用户头像，存储路径(表单用FileField字段，实现参考https://blog.csdn.net/liuredflash/article/details/79646678)
    photo = db.Column(db.String(64), default='default_icon.jpg')
    privilege = db.Column(db.Integer, default=2)  # 用户权限(普通用户2，普通管理员1，root管理员0)

    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))
    avatar_raw = db.Column(db.String(64))

    # 该用户撰写的影评(不需要级联删除)
    reviews = db.relationship(
        'Review',
        backref='user'
    )

    def set_password(self, password):
        """用来设置密码的方法，接受密码作为参数"""
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):
        """用于验证密码的方法，接受密码作为参数"""
        return check_password_hash(self.password_hash, password)  # 返回布尔值


# 影片分类先不做了，因为现在所有的影片都是电影
# class Category(db.Model):
#     """
#         影片分类：影片的名称不允许重复，因此name值将unique参数设为True
#         举例：(综艺、电影、动漫、纪录片、电视剧、儿童...)one to many
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), unique=True)
#     movies = db.relationship('')


# association table关联表(影片<->标签)
movie_tag = db.Table('movie_tag',
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                     db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')))


class Tag(db.Model):
    """
        影片标签：标签的名称不允许重复，因此name值将unique参数设为True
        举例：剧情、喜剧、短片...同一个影片可以有多个标签
    """
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)


class Movie(db.Model):
    """
        影片实体：影片名、封面图、剧情、发行日期、影片、片长、影片豆瓣评分、\
                标签Tag、分类Category
        注：影片类型好像需要建立新的表Category(分类)
    """
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # ID
    name = db.Column(db.String(50))  # 影片名
    # 图片应该也要加一个单独的类，存储在数据库中，电影与图片是一对多的关系，测试阶段用假数据代替
    image = db.Column(db.String(64), default='default.jpg')  # 封面图
    desc = db.Column(db.Text)  # 剧情
    release_date = db.Column(db.Date)  # 发行日期
    mins = db.Column(db.SmallInteger)  # 片长(该字段没用过，试一试...)
    score = db.Column(db.Float)  # 影片豆瓣评分
    # 影片标签(剧情、喜剧、短片...)many to many Movie<->Tag
    tags = db.relationship('Tag', secondary=movie_tag,
                           backref=db.backref('movies', lazy='dynamic'),
                           lazy='dynamic')
    # 影片分类(综艺、电影、动漫、纪录片、电视剧、儿童...)one分类 to many影片
    # 一部影片只对应一个分类，因此影片和分类是多对一关系
    # category_id = db.
    # Column(db.Integer, db.ForeignKey('Category.id'))

    # cascade：级联操作
    reviews = db.relationship(
        'Review',
        backref='movie',
        cascade='all, delete',
        passive_deletes=True
    )


class Review(db.Model):
    """
        影评实体：影评id、影评标题、影评内容、对应类型、喜欢数、不喜欢数、收藏数、举报数、转载链接
        注：影评与影片
    """
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)  # ID
    title = db.Column(db.String(64), unique=True)  # 影评标题
    content = db.Column(db.Text)  # 影评内容
    # 对应类型：1表示对应电影，2表示对应话题，默认为1(以后可能会有更多的类型)
    # 该字段考虑用新的表category替代，暂不考虑
    review_type = db.Column(db.Integer, default=1)
    # 最后修改时间(但是关于用户修改应该要有日志系统)
    modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    fav_nums = db.Column(db.Integer, default=0)  # 喜欢数
    dislike_nums = db.Column(db.Integer, default=0)  # 不喜欢数
    collect_nums = db.Column(db.Integer, default=0)  # 收藏数
    tipoff_nums = db.Column(db.Integer, default=0)  # 被举报数
    # 转载链接(至于为什么用TEXT字段，网上也是众说纷纭，暂且用TEXT吧，虽然资源占用较多
    # link = db.Column(db.TEXT)
    link = db.Column(db.String(255), default=None)

    # 外键：movie(级联删除)和user(不级联删除)均为一对多关系
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'))
    # movie = db.relationship('Movie', back_populates='reviews')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # 级联操作
    # comments = db.relationship('Comment', backref='review', cascade='all, delete', passive_deletes=True)
    comments = db.relationship(
        'Comment',
        back_populates='review',
        cascade='all, delete'
    )



class Comment(db.Model):
    """
        评论实体：评论id、评论内容、评论类型、添加时间、喜欢数、不喜欢数
    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 必须加主键
    content = db.Column(db.String(500))  # 这里与影评的不同是限制了字数为500，短评可不能像长评那么长
    comment_type = db.Column(db.Integer, default=1)  # 默认为1，即影评；2为...暂定
    # timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 添加时间(为什么要加index)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fav_nums = db.Column(db.Integer, default=0)
    dislike_nums = db.Column(db.Integer, default=0)
    # checked字段是为了防止垃圾评论和不当评论，当用户发表评论后，评论默认显示在影评中，管理员有权限将其撤回，则该字段为False
    checked = db.Column(db.Boolean, default=True)

    review_id = db.Column(db.Integer, db.ForeignKey('review.id', ondelete='CASCADE'))
    review = db.relationship('Review', back_populates='comments')

    # 添加replied_id字段，通过db.ForeignKey()设置一个外键指向自身的id字段
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 被回复评论（父对象）的标量关系属性replied的定义
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # replies = db.relationship('Comment', back_populates='replied', cascade='all')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')

    """
        参考：基本照抄下面的
        [flask实战-个人博客-程序骨架、创建数据库模型、临接列表关系](https://www.cnblogs.com/xiaxiaoxu/p/10816820.html)
    """


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
