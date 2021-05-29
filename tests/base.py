# -*- coding: utf-8 -*-

import unittest

from flask import url_for

from Xtime2 import create_app
from Xtime2.extensions import db
from Xtime2.models import Admin


class BaseTestCase(unittest.TestCase):
    """
        参考：https://read.helloflask.com/c9-test
    """
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def login(self, username=None, password=None):
        pass

    def logout(self):
        pass





