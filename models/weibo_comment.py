import time
import json
from . import ModelMixin
from . import db
from models.user import User


class WeiboComment(db.Model, ModelMixin):
    __tablename__ = 'weibo_comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(60))
    name = db.Column(db.String(40))
    created_time = db.Column(db.String(20), default=0)
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibos.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.comment = form.get('comment', '')
        self.name = form.get('name', '')
        self.weibo_id = form.get('weibo_id', '')
        self.user_id = form.get('user_id', '')
        self.created_time = dt

    def json(self):
        d = dict(
            id=self.id,
            comment=self.comment,
            name=self.name,
            created_time=self.created_time,
            weibo_id=self.weibo_id,
            user_id=self.user_id,
        )
        return d

    def error_message(self):
        if len(self.comment) <= 2:
            return '评论太短了，至少要 3 个字符'
        elif len(self.comment) >= 10:
            return '评论不能大于9个字符'

    def valid(self):
        return len(self.comment) > 0 and len(self.name) > 0

    def get_avatar(self):
        a = User.query.filter_by(username=self.name).first()
        if a is None:
            return '/uploads/default.png'
        return a.avatar
