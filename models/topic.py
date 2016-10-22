import time
from . import ModelMixin
from . import db
from . import timestamp
# from routes.user import current_user


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    created_time = db.Column(db.String(), default=0)

    # has relationship with comments
    comments = db.relationship('Comment', backref="topic")

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.created_time = dt
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.comments_num = 0
        # self.user_id = current_user.id


    def update(self, form):
        self.title = form.get('topic_title', '')
        self.title = form.get('topic_content', '')
        self.save()