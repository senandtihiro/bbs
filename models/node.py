import time
from . import ModelMixin
from . import db


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(50))
    created_time = db.Column(db.String(20), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topics = db.relationship('Topic', backref="node")

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.name = form.get('name', '')
        self.description = form.get('description')
        self.created_time = dt
        # self.user_id = current_user.id


    def update(self, form):
        self.name = form.get('node_name', '')
        self.save()