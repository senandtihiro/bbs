from models.weibo import Weibo
from models.weibo_comment import WeiboComment
from routes import *
from routes.user import current_user
from functools import wraps

main = Blueprint('weibo', __name__)

pyid = id
Model = Weibo


@main.route('/')
def index():
    print('weibo index was called')
    u = current_user()
    # if u is None:
    #     return redirect(url_for('user.login_view'))
    # 查找所有的 todo 并返回
    weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
    for weibo in weibo_list:
        weibo.comments_num = len(weibo.comments)
        print('weibo.comments', weibo.comments)
    # for i in weibo_list:
    #     i.comment = i.comments()
    #     for j in i.comment:
    #         j.avatar = j.get_avatar()
    #     i.comments_num = len(i.comment)
    #     i.avatar = i.get_avatar()
    return render_template('weibo_index.html', weibos=weibo_list)


def owner_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        print('owner required')
        u = current_user()
        if request.args.get('weibo_id') != u.id:
            print('not owner')
            abort(404)
        return function(*args, **kwargs)
    return f


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    t = Weibo(form)
    t.name = u.username
    if t.valid():
        t.save()
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 todo
    return redirect(url_for('.index'))


@main.route('/comment', methods=['POST'])
def comment():
    form = request.form
    u = current_user()
    c = WeiboComment(form)
    c.name = u.username
    c.user_id = u.id
    # c.weibo_id =
    if c.valid():
        c.save()
    return redirect(url_for('.index'))


@main.route('/delete/<int:weibo_id>')
def delete(weibo_id):
    """
    <int:todo_id> 的方式可以匹配一个 int 类型
    int 指定了它的类型，省略的话参数中的 todo_id 就是 str 类型

    这个概念叫做 动态路由
    意思是这个路由函数可以匹配一系列不同的路由

    动态路由是现在流行的路由设计方案
    """
    # 通过 id 查询 todo 并返回
    w = Weibo.query.get(weibo_id)
    # 删除
    w.delete()
    # 引用蓝图内部的路由函数的时候，可以省略名字只用 .
    return redirect(url_for('.index'))
