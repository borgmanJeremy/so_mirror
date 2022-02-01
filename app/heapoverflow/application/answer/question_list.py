from flask import Blueprint
from flask import render_template

question_list_bp = Blueprint('question_list_bp', __name__,
                         template_folder='templates',
                         static_folder='static')

@question_list_bp.route('/question_list')
def index():
    return render_template('question_list.html')