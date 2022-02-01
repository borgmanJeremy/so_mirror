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
        res = get_questions(search_term)
        for elem in res:
            elem['body'] =  elem['body'].partition('\n')[0]
        return render_template('question_list.html', res=res)
    else: 
        return render_template('home.html')