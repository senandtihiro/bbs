from models.comment import Comment
from routes import *
from routes.user import current_user

main = Blueprint('comment', __name__)

Model = Comment

@main.app_context_processor
def inject_permissions():
    return dict(u=current_user)

@main.route('/add', methods=['POST'])
def add():
    print('comment add was called')
    form = request.form
    m = Model(form)
    m.topic_id = int(form.get('topic_id'))
    m.save()
    return redirect(url_for('topic.show', id=m.topic_id))



