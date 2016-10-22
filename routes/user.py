from models.user import User
from routes import *
from app import UPLOAD_FOLDER
from flask import Flask
from functools import wraps
# from app import UPLOAD_FOLDER

main = Blueprint('user', __name__)

pyid = id
Model = User

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        # print('user', u)
        return u


@main.route('/')
def login_view():
    u = current_user()
    # print('u:', u)
    if u is not None:
        return redirect('/node/show')
        # return render_template('node.html')
    return render_template('user_login.html')

@main.route('/register_view')
def register_view():
    return render_template('user_register.html')

@main.route('/register', methods=['GET','POST'])
def register():
    print('register was called')
    form = request.form
    u = User(form)
    if u.valid():
        print('u is valid')
        # u.save()
        print('u.username',u.username)
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


# @main.route('/upload_avatar', methods=['POST'])
# def upload_avatar():
#     u = current_user()
#     file = request.files['file']
#     if file:
#         filename = u.username + file.filename
#         file.save(os.path.join(UPLOAD_FOLDER, filename))
#     # return redirect(url_for('uploaded_file', filename=filename))
#     return redirect(url_for('update_avatar', filename=filename))

# @main.route('/uploads/<filename>')
# def uploaded_file(filename):
#     print('uploaded_file was called', uploaded_file)
#     return send_from_directory(UPLOAD_FOLDER, filename)


# @main.route('/update_avatar/<filename>')


@main.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    print('upload_avatar was called')
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('.update_avatar', filename=filename))


@main.route('/update_avatar/<string:filename>', methods=['GET', 'POST'])
def update_avatar(filename):
    u = current_user()
    if u.change_avatar(filename):
        print('修改成功')
    else:
        print('用户头像修改失败')
    return redirect('/user/profile')





@main.route('/profile', methods=['GET'])
# @login_required
def profile():
    print('frofile was called')
    u = current_user()
    if u is not None:
        # print('profile', u.id, u.username, u.password)
        return render_template('profile.html', user=u)
    else:
        abort(401)
