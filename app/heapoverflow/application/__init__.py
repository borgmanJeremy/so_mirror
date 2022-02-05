from flask import Flask
import psycopg2

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    app.conn = psycopg2.connect(
        host=app.config['SQL_URI'], 
        database=app.config['SQL_DB'], 
        port=app.config['SQL_PORT'],
        user=app.config['SQL_USER'], 
        password=app.config['SQL_PASSWORD'])

    with app.app_context():
        from .home      import home
        from .question  import question
        from .question_list    import question_list

        app.register_blueprint(home.home_bp)
        app.register_blueprint(question.question_bp)
        app.register_blueprint(question_list.question_list_bp)
        return app