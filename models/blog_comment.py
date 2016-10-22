import time
import json
from . import ModelMixin
from . import db


class BlogComment(db.Model, ModelMixin):
    __tablename__ = 'blog_comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))
    name = db.Column(db.String(100))
    created_time = db.Column(db.String(20), default=0)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.comment = form.get('comment', '')
        self.name = form.get('name', '')
        self.blog_id = form.get('blog_id', '')
        self.user_id = form.get('user_id', '')
        self.created_time = dt

    def valid(self):
        return len(self.comment) > 0 and len(self.name) > 0

    # def get_avatar(self):
    #     a = User.query.filter_by(username=self.name).first()
    #     if a is None:
    #         return '/uploads/default.png'
    #     return a.avatar

    def json(self):
        d = {
            'id': self.id,
            'comment': self.comment,
            'created_time': self.created_time,
            'blog_id': self.blog_id,
            'user_id': self.user_id,
            'name': self.name,
            # 'avatar': self.avatar,
        }
        # return json.dumps(d, ensure_ascii=False)
        return d


    def error_message(self):
        if len(self.comment) <= 2:
            return '评论太短了，至少要 3 个字符'
        elif len(self.comment) >= 10:
            return '评论不能大于9个字符'

