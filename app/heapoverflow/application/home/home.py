from flask import Blueprint, request
from flask import render_template
from sql_query import *

home_bp = Blueprint('home_bp', __name__,
                         template_folder='templates',
                         static_folder='static')

@home_bp.route('/', methods=['GET', 'POST'])
@home_bp.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['keyword']
        question_list = get_questions(search_term)
        for elem in question_list:
            accepted_answer = get_answer_by_id(elem["ans_id"])
            if accepted_answer != None:
                elem['answer'] = accepted_answer['body'].partition('\n')[0]
            else:
                elem['answer'] = "No Accepted Answer"

            elem['body'] =  elem['body'].partition('\n')[0]
        return render_template('question_list.html', question_list=question_list)
    else: 
        return render_template('home.html')