from models.topic import Topic
from models.node import Node
from routes import *
from routes.user import current_user
from functools import wraps
main = Blueprint('topic', __name__)

Model = Topic

# @main.app_context_processor
# def inject_permissions():
#     return dict(u=current_user)


# def login_required(f):
#     @wraps(f)
#     def function(*args, **kwargs):
#         print('login required')
#         u = current_user()
#         if u is None:
#             return redirect('/user/login')
#         return function(*args, **kwargs)
#     return f


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        print('login required')
        u = current_user()
        if u is None:
            return redirect('/user/login')
        return f(*args, **kwargs)
    return function


@main.route('/<int:id>')
def index(id):
    print('topic/index was called')
    # ms = Model.query.all()
    m = Model.query.get(id)
    print('debug topic:', m)
    m.view += 1
    m.save()
    # node = Node.query.get(m.node_id)
    return render_template('topic_index.html', topic=m)


@main.route('/new')
@login_required
def new():
    print('topic.new was called')
    u = current_user()
    print('current_user:', current_user())
    # if u is None:
    #     return render_template('topic_new.html')
    # else:
    return render_template('topic_new.html')
    # return render_template('topic_new.html', u=u)


# @main.route('/new')
# def new():
#     print('topic.new was called')
#     u = current_user()
#     if u is not None:
#         return render_template('topic_new.html')
#     else:
#         return redirect(url_for('user.login_view'))


@main.route('/<int:id>')
def show(id):
    print('topic.show was called')
    # ts为所有的topics
    ts = Model.query.all()

    # t = Model.query.get(id)
    # 有了关系之后关联的字段就不必要给出来了
    # node = Node.query.get(t.node_id)
    return render_template('topic.html')
    # return render_template('topic.html', topic_list=ts)

# @main.route('/')
# def show():
#     print('topic.show was called')
#     ts = Model.query.all()
#     # t = Model.query.get(id)
#     # 有了关系之后关联的字段就不必要给出来了
#     # node = Node.query.get(t.node_id)
#     return render_template('topic.html', topic_list=ts)

@main.route('/edit/<id>')
def edit(id):
    t = Model.query.get(id)
    return render_template('topic_edit.html', topic=t)


@main.route('/add', methods=['POST'])
def add():
    print('topic.add was called')
    form = request.form
    t = Model(form)
    u = current_user()
    t.node_id = int(form.get('node_id'))
    t.user_id = u.id
    t.save()
    print('topic',t)
    return redirect(url_for('.index', id=t.id))


@main.route('/comment/add', methods=['POST'])
def comment_add():
    form = request.form
    m = Model(form)
    m.save()
    return redirect(url_for('topic.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('.index', id=id))



