from routes.user import current_user
from routes import *
from models.weibo import Weibo
from models.weibo_comment import WeiboComment
from models.blog_comment import BlogComment
from functools import wraps
# from routes.topic import login_required

# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('api', __name__)


@main.app_context_processor
def inject_permissions():
    return dict(u=current_user)


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        print('login required')
        u = current_user()
        if u is None:
            return redirect('/user/login')
        return f(*args, **kwargs)
    return function



def owner_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        # your code
        print('owner required')
        weiboId = request.args.get('weibo_id')
        u = current_user()
        print('current_user', current_user())
        r = {
            'data': []
        }
        if u.id != weiboId:
            r['success'] = False
            r['message'] = '只能删除自己发的微博'
        return function(*args, **kwargs)
    return f


@main.route('/weibo/add', methods=['POST'])
# @login_required
def add():
    print('api.py weibo add was called')
    form = request.form
    u = current_user()
    r = {
        'data': []
    }
    if u is None:
        print('u is none')
        r['success'] = False
        r['message'] = '请先登录'
        # return render_template('user_login.html')
        # return redirect(url_for('user.login_view'))
    else:
        t = Weibo(form)
        t.name = u.username
        t.user_id = u.id
        r = {
            'data': []
        }
        if t.valid():
            t.save()
            print('api.weibo.add.r', r)
            print('api.weibo.add.t', t)
            r['success'] = True
            r['data'] = t.json()
        else:
            r['success'] = False
            message = t.error_message()
            r['message'] = message
        print('api.py weibo.add.response', r)
    return json.dumps(r, ensure_ascii=False)


# /api/weibo/update
@main.route('/weibo/update', methods=['POST'])
def update():
    form = request.form
    print('update中的form是：', form)
    # u = current_user()
    # t = Weibo(form)
    weibo_id = int(form.get('id', -1))
    print('微博的ID：',weibo_id)
    w = Weibo.query.get(weibo_id)
    print('update中取到的微博：',w)
    weibo = form.get('weibo', '')
    u = current_user()
    r = {
        'data': []
    }
    if u.id != w.user_id:
        print('user.id', u.id)
        print('weibo.id', w.user_id)
        r['success'] = False
        r['message'] = '限博主本人'
    else:
        print('get到的微博：',weibo)
        w.weibo = weibo
        w.save()
        print('新微博内容：',w.weibo)
        r['success'] = True
        r['data'] = w.json()
        print('r的内容',r)
    return json.dumps(r, ensure_ascii=False)


# @main.route('/weibo/delete/<int:weibo_id>', methods=['GET'])
# @login_required
# @owner_required
# def delete(weibo_id):
#     print('api.weibo.deleted was called')
#     w = Weibo.query.get(weibo_id)
#     # u = current_user()
#     # r = {
#     #     'data': []
#     # }
#     # if u.id != w.user_id:
#     #     print('user.id', u.id)
#     #     print('weibo.user_id', w.user_id)
#     #     r['success'] = False
#     #     r['message'] = '只能删除自己发的微博'
#     # else:
#     w.delete()
#     r = {
#         'success': True,
#         'data': w.json(),
#     }
#     return json.dumps(r, ensure_ascii=False)




@main.route('/weibo/delete/<int:weibo_id>', methods=['GET'])
def delete(weibo_id):
    print('api.weibo.deleted was called')
    w = Weibo.query.get(weibo_id)
    u = current_user()
    r = {
        'data': []
    }
    if u is None:
        print('u is none')
        r['success'] = False
        r['message'] = '请先登录'
        # return render_template('user_login.html')
        # return redirect(url_for('user.login_view'))
    else:
        if u.id != w.user_id:
            print('user.id', u.id)
            print('weibo.user_id', w.user_id)
            r['success'] = False
            r['message'] = '只能删除自己发的微博'
        else:
            w.delete()
            r = {
                'success': True,
                'data': w.json(),
            }
    return json.dumps(r, ensure_ascii=False)

@main.route('/weibo/comment', methods=['GET','POST'])
def weibo_comment():
    print('api.blog.comment was called')
    form = request.form
    u = current_user()
    c = WeiboComment(form)
    c.name = u.username
    c.user_id = u.id
    c.weibo_id = int(form.get('weibo_id', -1))
    print('评论微博的id：',c.weibo_id)
    r = {
        'data': []
    }
    if c.valid():
        c.save()
        print('评论保存成功',c)
        r['success'] = True
        r['data'] = c.json()
    else:
        r['success'] = False
        message = c.error_message()
        r['message'] = message
    print('评论中r的内容r的内容：：', r)
    return json.dumps(r, ensure_ascii=False)


@main.route('/blog/comment', methods=['GET','POST'])
def comment():
    print('api.blog.comment was called')
    form = request.form
    u = current_user()
    c = BlogComment(form)
    c.name = u.username
    c.user_id = u.id
    c.blog_id = int(form.get('blog_id', -1))
    print('评论博客的id：',c.blog_id)
    r = {
        'data': []
    }
    if c.valid():
        c.save()
        print('评论保存成功')
        r['success'] = True
        r['data'] = c.json()
    else:
        r['success'] = False
        message = c.error_message()
        r['message'] = message
    print('评论中r的内容r的内容：：', r)
    return json.dumps(r, ensure_ascii=False)



