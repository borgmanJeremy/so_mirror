from flask import Blueprint, request
from flask import render_template

from sql_query import get_answers_for_question, get_question_details

question_bp = Blueprint('question_bp', __name__,
                        template_folder='templates',
                        static_folder='static')


@question_bp.route('/question')
def index():
    id = request.args.get('id')
    question = get_question_details(id)
    answers  = get_answers_for_question(question['id'])

    return render_template('question.html', question=question, answers=answers, num_ans=len(answers))
