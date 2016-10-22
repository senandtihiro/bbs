import time
from . import ModelMixin
from . import db
from . import timestamp


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    title = db.Column(db.String(100))
    name = db.Column(db.String(100))
    created_time = db.Column(db.String(20), default=0)
    comments = db.relationship('BlogComment', backref="blog")


    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.name = form.get('name', '')
        self.created_time = dt
        self.comments = []
        self.comments_num = 0

    def valid(self):
        return len(self.title) > 0 and len(self.content) > 0


    def json(self):
        d = dict(
            id= self.id,
            comment=self.content,
            name=self.name,
            created_time=self.created_time,
            # user_id=self.user_id,
            # avatar=self.get_avatar(),
            comments_num=len(self.comments()),
        )
        return d