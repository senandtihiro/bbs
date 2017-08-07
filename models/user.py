from models import *

from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12))
    password = db.Column(db.String(12))
    avatar = db.Column(db.String(1000), default='/static/avatar/default.png')
    created_time = db.Column(db.String(20), default=0)
    # email = db.Column(db.String())
    is_administrator = db.Column(db.Boolean, default=False, index=True)
    nodes = db.relationship('Node', backref='user')
    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')
    blog_comments = db.relationship('BlogComment', backref='user')
    weibo_comments = db.relationship('WeiboComment', backref='user')
    follower_count = db.Column(db.Integer)
    # follower =


    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.created_time = dt
        self.follower_count = 0


    # def get_avatar(self, size=100, default='identicon', rating='g'):
    #     # if request.is_secure:
    #     #     url = 'https://secure.gravatar.com/avatar'
    #     # else:
    #     #     url = 'http://www.gravatar.com/avatar'
    #     url = 'http://www.gravatar.com/avatar'
    #     hash = hashlib.md5(str(self.id).encode('utf-8')).hexdigest()
    #     return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
    #         url = url,
    #         hash = hash,
    #         size = size,
    #         default = default,
    #         rating = rating
    #     )

    def valid(self):
        print('valid was called')
        user = User.query.filter_by(username=self.username).first()
        # print('user', user)
        # if user is not None:
        #     return False
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False


    # def get_avatar(self, filepath):
    #     with open(filepath, 'rb') as f:
    #         self.avatar = f.read()
    #     return self.avatar

    # def change_avatar(self, filename):
    #     self.avatar = send_from_directory('uploads/', filename)
    #     self.save()
    def change_avatar(self, avatar):
         print('change_avatar was called')
         print('length of avatar > 2?', len(avatar))
         print('change_avatar was called')
         if len(avatar) > 2:
             self.avatar = avatar
             self.save()
             return True
         else:
             return False

    # def valid_login(self, u):
    #     if u is not None:
    #         username_equals = u.username == self.username
    #         password_equals = u.password == self.password
    #         return username_equals and password_equals
    #     else:
    #         return False
    #
    # # 验证注册用户的合法性的
    # def valid(self):
    #     valid_username = User.query.filter_by(username=self.username).first() == None
    #     valid_username_len = len(self.username) >= 6
    #     valid_password_len = len(self.password) >= 6
    #     valid_captcha = self.captcha == '3'
    #     msgs = []
    #     if not valid_username:
    #         message = '用户名已经存在'
    #         msgs.append(message)
    #     elif not valid_username_len:
    #         message = '用户名长度必须大于等于 6'
    #         msgs.append(message)
    #     elif not valid_password_len:
    #         message = '密码长度必须大于等于 6'
    #         msgs.append(message)
    #     elif not valid_captcha:
    #         message = '验证码必须输入 3'
    #         msgs.append(message)
    #     status = valid_username and valid_username_len and valid_password_len and valid_captcha
    #     return status, msgs
