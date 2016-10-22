from models.node import Node
from models.user import User
from models.topic import Topic
from routes import *
from routes.user import current_user

# for decorators
from functools import wraps

main = Blueprint('node', __name__)

Model = Node


# def admin_required(f):
#     @wraps(f)
#     def function(*args, **kwargs):
#         # your code
#         print(request.args)
#         print('admin required')
#         u = current_user()
#         if u.is_administrator:
#             print('current user is administrator')
#         else:
#             print('current user is not administrator')
#             abort(410)
#         # if request.args.get('uid') != '1':
#         #     print('not admin')
#         #     abort(404)
#         # return f(*args, **kwargs)
#     return f


@main.route('/')
def index():
    print('执行到node根目录')
    ms = Model.query.all()
    # print('ms:', ms)
    return render_template('node_index.html', node_list=ms)

# @main.route('/show')
# def show():
#     print('执行到node根目录')
#     ms = Model.query.all()
#
#     node = Node.query.first()
#     # print('ms:', ms)
#     return render_template('node_all.html', node_list=ms,node=node)

@main.route('/show')
def show():
    print('执行到node/show目录')
    ms = Model.query.all()
    node = Node.query.first()
    for t in node.topics:
        t.comments_num = len(t.comments)
        print('t.comments',t.comments)
    print('topic.comments_num:', t.comments_num)
    return render_template('node_all.html', node_list=ms, node=node)

@main.route('/new', methods=['GET', 'POST'])
def new():
    print('node.new was called')
    u = current_user()
    print('u.is_administrator', u.is_administrator)
    if u.is_administrator:
        print('current user is administrator')
    else:
        print('current user is not administrator')
        abort(410)
    return render_template('node_new.html')


@main.route('/showSinglePage/<int:id>')
def showSinglePage(id):
    nodes = Model.query.all()
    node = Model.query.get(id)
    print('node',node)
    # username = node.user.username
    # print('username', username)
    for t in node.topics:
        t.comments_num = len(t.comments)
        print('topic.comments_num:', t.comments_num)
        print('topic.comments:', t.comments)
    return render_template('node_all.html', node_list=nodes, node=node)


@main.route('/showAllPages')
def showAllPages():
    nodes = Node.query.all()
    return render_template('node_all.html', nodes=nodes)



@main.route('/edit/<id>')
def edit(id):
    n = Model.query.get(id)
    return render_template('node_edit.html', node=n)


@main.route('/add', methods=['POST'])
def add():
    print('node add was called')
    form = request.form
    m = Model(form)
    u = current_user()
    m.user_id = u.id
    m.save()
    return redirect(url_for('.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    n = Model.query.get(id)
    n.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
# @admin_required
def delete(id):
    t = Model.query.get(id)
    t.delete()
    return redirect(url_for('.index'))
