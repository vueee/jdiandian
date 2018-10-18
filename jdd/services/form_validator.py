from wtforms import Form, StringField, SelectField, SelectMultipleField, TextAreaField, DateField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
'''
class TagListField(Form):
    widget = TextInput()
    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []
'''


class RegisterForm(Form):
    name = StringField('name', [Length(min=1, max=20)])
    email = StringField('email', [
        Email(),
        Length(min=6, max=50)])
    password = PasswordField('password', [
        Length(min=6, max=50),
        EqualTo('confirm', message='Password must match!')
    ])
    confirm = PasswordField('confirm')
    accept = BooleanField('I agree the user policy!', [DataRequired()])


class LoginForm(Form):
    email = StringField('email', [
        Email(),
        Length(min=6, max=50)])
    password = PasswordField('password', [Length(min=6, max=50)])


class ResetForm(Form):
    email = StringField('email', [
        Email(),
        Length(min=6, max=50)])
    newpasswd = PasswordField('newpasswd', [Length(min=6, max=50)])


'''
# images = uploadSet('images',IMAGES)
class FileForm(Form):
    file = FileField('file',[
        FileRequired(),
        FileAllowed(images,'Images only')])
'''


class NewPostForm(Form):
    name = StringField('name', [Length(max=50)])
    cover = StringField('cover', [Length(max=999)])
    title = StringField('title', [Length(min=1, max=200)])
    summary = StringField('summary', [Length(max=2000)])
    tags = StringField('tags', [Length(max=200)])
    body = TextAreaField('body', [Length(min=10)])


class UserInfoForm(Form):
    name = StringField('name', [Length(max=20)])
    phone = StringField('phone', [Length(max=26)])
    summary = TextAreaField('summary')
    sex = SelectField('sex', choices=[('', '请选择'), ('男', '男'), ('女', '女')])
    birthday = DateField('birthday', format='%Y-%m-%d')
    marriage = SelectField('marriage', choices=[(
        '', '请选择'), ('二人殿堂', '二人殿堂'), ('单身贵族', '单身贵族')])
    hobby = SelectMultipleField('Hobby', choices=[
        ('运动', '运动'),
        ('IT', '科技'),
        ('摄影', '摄影'),
        ('音乐', '音乐'),
        ('跳舞', '跳舞'),
        ('二次元', '二次元'),
        ('玩游戏', '玩游戏'),
        ('美食', '美食'),
        ('读书', '读书'),
        ('文学', '文学'),
        ('绘画', '绘画'),
        ('电影', '电影'),
        ('聊天', '聊天'),
    ])

