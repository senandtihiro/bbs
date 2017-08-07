from models.user import User
from routes import *
from app import UPLOAD_FOLDER
from flask import Flask
from functools import wraps
from models.topic import Topic
from models.comment import Comment

# from routes.api import login_required
# from app import UPLOAD_FOLDER

main = Blueprint('user', __name__)

pyid = id
Model = User


@main.route('/')
def login_view():
    u = current_user()
    # print('u:', u)
    if u is not None:
        return redirect('/')
    return render_template('user_login.html')


@main.route('/register_view')
def register_view():
    return render_template('user_register.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    print('register was called')
    form = request.form
    u = User(form)
    if u.valid():
        print('u is valid')
        # u.save()
        print('u.username', u.username)
        if u.username == 'ahe':
            u.is_administrator = True
            print('u.is_administrator', u.is_administrator)
        else:
            u.is_administrator = False
        u.save()
        # print('u:',u)
    else:
        abort(400)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = request.form
    u = User(form)
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    user = User.query.filter_by(username=u.username).first()
    print('user', user)
    if user is not None and user.validate_login(u):
        print('登录成功')
        session['user_id'] = user.id
    else:
        print('登录失败')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/logout')
# @login_required
def logout():
    print('logout was called')
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    session.pop('user_id')
    user = current_user()
    print('logout u', user)
    if user is not None:
        print('登出失败')
    else:
        print('登出成功')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/update_password', methods=['POST'])
def update_password():
    u = current_user()
    password = request.form.get('password', '123')
    if u.change_password(password):
        print('修改成功')
    else:
        print('用户密码修改失败')
    return redirect('/user/profile')


@main.route('/upload_avatar', methods=['POST'])
def upload_file():
    print('upload')
    # 通过 request.files 访问上传的文件
    # uploaded 是上传时候的文件名
    f = request.files.get('uploaded')
    u = current_user()
    print(request)
    print('upload, ', request.files)
    if f:
        filename = u.username + f.filename
        print('filename, ', filename)
        path = UPLOAD_FOLDER + filename
        print(os.getcwd())
        f.save(path)
        # full_path =
        u.avatar = '/' + path
        # u.avatar = path
        u.save()
        print('debug path:', u.avatar)
        print('file was successfully saved')
        return redirect('/user/profile')
    else:
        return '<h1>没有上传</h1>'

# @main.route('/upload_avatar', methods=['POST'])
# def upload_avatar():
#     print('upload_avatar was called')
#     file = request.files['file']
#     if file:
#         filename = file.filename
#         file.save(os.path.join(UPLOAD_FOLDER, filename))
#     return redirect(url_for('.update_avatar', filename=filename))
#
#
# @main.route('/update_avatar/<string:filename>', methods=['GET', 'POST'])
# def update_avatar(filename):
#     u = current_user()
#     if u.change_avatar(filename):
#         print('修改成功')
#     else:
#         print('用户头像修改失败')
#     return redirect('/user/profile')


@main.route('/profile', methods=['GET'])
@login_required
def profile():
    print('frofile was called')
    u = current_user()
    if u is not None:
        # print('profile', u.id, u.username, u.password)
        return render_template('profile.html', user=u)


@main.route('/info/<int:id>', methods=['GET'])
# @login_required
def user_info(id):
    print('user_info was called')
    u = User.query.get(id)
    topics = Topic.query.filter_by(user_id=id).all()
    comments = Comment.query.filter_by(user_id=id).all()
    print('debug all topics by this user:', topics)
    # user = User.query.filter_by(username=u.username).first()

    # print('debug u:', u)
    return render_template('user_info.html', user=u, topics=topics, comments=comments)
    # return render_template('user_info.html', user=u)
    # u = ()
    # if u is not None:
    #     # print('profile', u.id, u.username, u.password)
    #     return render_template('profile.html', user=u)


# 处理关注人功能，前面的id是被关注者的id，后面的id是当前用户的id即关注者的id
@main.route('/follow/<int:id>', methods=['GET'])
# @login_required
def user_follow(id):
    print('user_follow was called')
    print('current_user_id:', request.args.get('once'))
    # request.args.get('once')
    print('current_user:', current_user())
    c_user = current_user()
    c_user.follower_count += 1
    c_user.save()
    u = User.query.get(id)
    topics = Topic.query.filter_by(user_id=id).all()
    comments = Comment.query.filter_by(user_id=id).all()
    return render_template('user_info.html', user=u, topics=topics, comments=comments)










