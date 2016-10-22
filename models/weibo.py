from models import *


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    weibo = db.Column(db.String(40))
    name = db.Column(db.String(20))
    created_time = db.Column(db.String(20), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('WeiboComment', backref="weibo")

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.weibo = form.get('weibo', '')
        self.name = form.get('name', '')
        self.created_time = dt
        self.user_id = form.get('user_id', '')
        self.comments = []
        self.comments_num = 0
        print('self.__init__ was called,comments_num=:', self.comments_num)
        print('self.__init__ was called,comments:', self.comments)
        print('self.__init__ was called,len(comments:)', len(self.comments))


    def valid(self):
        return len(self.weibo) > 2 and len(self.weibo) < 10 and len(self.name) > 0

    # def comments(self):
    #     cs = Comment.query.filter_by(weibo_id=self.id).all()
    #     return cs

    # def get_avatar(self):
    #     a = User.query.filter_by(username=self.name).first()
    #     if a is None:
    #         return 'http://vip.cocode.cc/uploads/avatar/default.png'
    #     return a.avatar

    def error_message(self):
        if len(self.weibo) <= 2:
            return '微博太短了，至少要 3 个字符'
        elif len(self.weibo) >= 10:
            return '微博不能大于9个字符'
        elif self.user_id is None:
            return '请先登录'


    def json(self):
        d = dict(
            id=self.id,
            weibo=self.weibo,
            name=self.name,
            created_time=self.created_time,
            user_id = self.user_id,
            # avatar = self.avatar,
            comments_num=len(self.comments),
        )
        return d