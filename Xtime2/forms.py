# -*- coding: utf-8 -*-
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, \
    HiddenField, BooleanField, PasswordField, RadioField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo, \
    Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

from datetime import date, datetime

from Xtime2.models import Admin, User


class LoginForm(FlaskForm):
    """
        用户登录表单
    """
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(1, 30)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    """
        用户注册表单
        注：实现注册过程中遇到的坑
        1、form.validate_on_submit() 验证总为False，大概率是代码哪里写错了
        2、接上条，比如form表框如果有中文，最好前面加上u；form表单加上{{ form.csrf_token }}；定义表单时(forms.py)加上validators=[DataRequired()]
        3、解决第2条可以通过在html页面中渲染error消息解决，很管用，参考https://www.cnblogs.com/xiaxiaoxu/p/10513796.html
        仍需要解决的问题：
        1、注册失败(比如邮箱格式错误)后表单数据全部消失，这不应该
        2、error提示应该人性化
        3、注册验证还应检验用户名/邮箱是否已经存在
        ...
    """

    # 用户姓名表框
    name = StringField(
        label=u'姓名',
        validators=[
            DataRequired()
        ]
    )

    # 邮箱表框
    email = StringField(
        label=u'邮箱',
        validators=[
            DataRequired(),
            Length(1, 254),
            Email(message=u'邮箱格式不合法')
        ]
    )

    # 用户名表框 文本输入框，必填
    username = StringField(
        label=u'用户名',  # 标签
        validators=[  # 验证方式
            DataRequired(),  # 不能为空
            Length(1, 20)
        ]
    )

    # 密码表框
    password = PasswordField(
        label=u'密码',
        validators=[
            DataRequired(),
            Length(6, 16, message=u'密码长度应在6~16位'),
            EqualTo(fieldname='confirm', message=u'两次输入不一致')
        ]
    )

    # 确认密码表框
    confirm = PasswordField(
        label=u'确认密码',
        validators=[
            DataRequired()
            # EqualTo(fieldname='password', message='两次输入不一致')
        ]
    )

    # 注册按钮
    submit = SubmitField(
        label=u'注册'
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(u'邮箱地址已存在')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在')

    # privilege = None                      # 用户权限(该字段暂时先不考虑，管理员与普通用户应该独立)

    # # 接受许可(Checkbox类型，加上default='checked'即默认是选上的 )
    # accept_terms = BooleanField(
    #     label='I accept the Terms of Use',
    #     default='checked',
    #     validators=[DataRequired()]
    # )


class ForgetPasswordForm(FlaskForm):
    pass
    # email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    # submit = SubmitField()


class ResetPasswordForm(FlaskForm):
    pass
    # email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    # password = PasswordField('Password', validators=[DataRequired(), Length(6, 16), EqualTo('confirm')])
    # confirm = PasswordField('Confirm', validators=[DataRequired(), Length(6, 16)])
    # submit = SubmitField()


class EditProfileForm(FlaskForm):
    """
        个人中心编辑表单，包括了User实体所有可编辑的字段(id字段、name字段不可编辑)
        另：密码、邮箱等字段单独编辑

    """

    name = StringField(u'姓名', validators=[DataRequired(), Length(1, 20)])
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 254), Email(u'邮箱格式不合法')])
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 20)])
    phone = StringField(u'电话', validators=[DataRequired('请输入电话'), Regexp('1\d{10}')])   # 正则匹配
    # 示例：Gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    gender = RadioField(u'性别', choices=[('M', 'male'), ('F', 'female')])
    # 日期字段datetime.date(year=2018, month=2, day=20)2018-02-20
    # 出生日期(文本输入框，必须输入是"年-月-日"格式的日期)
    birthday = DateField(label=u'出生日期', format='%Y-%m-%d', default=date(1999, 11, 24))
    address = None  # 地址(暂时不用)
    signature = StringField(u'个性签名', validators=[DataRequired(), Length(1, 50)])
    introduction = TextAreaField(u'个人描述', validators=None)  # 还应该限制字数
    # 用户头像，存储路径(表单用FileField字段，实现参考https://blog.csdn.net/liuredflash/article/details/79646678)
    photo = FileField(
        label=u'头像',
        validators=[
            # 文件必须选择
            FileRequired(),
            # 指定文件上传的格式
            FileAllowed(upload_set=['png', 'jpg'], message='请上传图片')])
    submit = SubmitField(u'注册')

