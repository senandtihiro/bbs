from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask.ext.login import LoginManager

from models import db

from flask import render_template


app = Flask(__name__)
# db_path = 'bbs.sqlite'
db_path = 'mysql://root:111111@localhost/bbs'
# UPLOAD_FOLDER = 'uploads/'
UPLOAD_FOLDER = 'static/avatar/'
manager = Manager(app)

# login_manager = LoginManager()
# login_manager.login_view = 'user.login'


def register_routes(app):
    # from routes.todo import main as routes_todo
    from routes.node import main as routes_node
    from routes.topic import main as routes_topic
    from routes.user import main as routes_user
    from routes.weibo import main as routes_weibo
    from routes.blog import main as routes_blog
    from routes.comment import main as routes_comment
    from routes.api import main as routes_api

    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_node, url_prefix='/node')
    app.register_blueprint(routes_topic, url_prefix='/topic')
    # app.register_blueprint(routes_blog, url_prefix='/blog')
    app.register_blueprint(routes_blog)
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_comment, url_prefix='/comment')
    app.register_blueprint(routes_api, url_prefix='/api')
    # app.register_blueprint(routes_todo, url_prefix='/todo')

def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:111111@localhost:3306/bbs?charset=utf8'
    db.init_app(app)
    # login_manager.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


@app.errorhandler(404)
def error404(e):
    return render_template('404.html')


@app.errorhandler(410)
def error404(e):
    return render_template('410.html')

@manager.command
def server():
    print('server run')
    # app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5001,
    )
    app.run(**config)


def configure_manager():

    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()


