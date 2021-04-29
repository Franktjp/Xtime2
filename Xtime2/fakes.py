# -*- coding: utf-8 -*-
import random

from faker import Faker
from datetime import date
# from sqlalchemy.exc import IntegrityError
from Xtime2.models import Admin, User

from Xtime2.extensions import db

fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        name='Franktjp'
    )
    admin.set_password('123')
    db.session.add(admin)
    db.session.commit()


def fake_user():
    user1 = User(
        name='邰阶平',
        username='Franktjp',
        email='Franktjp@1.com'
    )
    user1.set_password('12345')
    user2 = User(
        name='黄药师',
        username='黄老邪',
        email='huanglaoxie@1.com'
    )
    user2.set_password('12345')
    user3 = User(
        name='丘处机',
        username='傻逼',
        email='shabi@1.com'
    )
    user3.set_password('12345')
    user4 = User(
        name='金轮法王',
        username='哟西',
        email='yoxi@1.com',
        phone='19946255605',
        gender=1,
        birthday=date(1999, 11, 24),
        signature='嘤嘤嘤',
        introduction='嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤嘤怪'
    )
    user4.set_password('12345')

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()


def fake_movie():
    pass


def fake_comment():
    pass


def fake_topic():
    pass


def fake_review():
    pass
