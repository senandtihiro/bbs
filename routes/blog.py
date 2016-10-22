from routes import *
from routes.user import current_user
from models.blog import Blog
from models.blog_comment import BlogComment

main = Blueprint('blog', __name__)

pyid = id


@main.app_context_processor
def inject_permissions():
    return dict(u=current_user)


@main.route('/')
def index():
    u = current_user()
    # if u is None:
    #     return redirect(url_for('user.login_view'))
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    for blog in blogs:
        blog.comments_num = len(blog.comments)
    # for i in blogs:
    #     i.comment = i.comments()
    #     for j in i.comment:
    #         j.avatar = j.get_avatar()
    #     i.comments_num = len(i.comment)
    return render_template('blog_index.html', blogs=blogs)


@main.route('/new')
def new():
    print('blog new was called')
    u = current_user()
    if u is not None:
        return render_template('blog_add.html')
    else:
        return redirect(url_for('user.login_view'))


@main.route('/add', methods=['POST'])
def add():
    print('blog add was called')
    form = request.form
    u = current_user()
    b = Blog(form)
    # b.name = '3000'
    if b.valid():
        b.save()
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 todo
    return redirect(url_for('.index'))


@main.route('/comment', methods=['GET', 'POST'])
def comment():
    print('blog.comment was called ')
    u = current_user()
    if u is not None:
        form = request.form
        c = BlogComment(form)
        c.name = u.username
        if c.valid():
            c.save()

            print('blogcomment was saved', c)
    # c.avatar = c.get_avatar()
    return c.json()


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
    w = Blog.query.get(weibo_id)
    # 删除
    w.delete()
    # 引用蓝图内部的路由函数的时候，可以省略名字只用 .
    return redirect(url_for('.index'))
