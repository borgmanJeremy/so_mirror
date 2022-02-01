from flask import current_app as app


def get_questions(search_term):
    cursor = app.conn.cursor()
    cursor.execute("""
    SELECT id, score, body
    FROM question
    WHERE ts @@ phraseto_tsquery(%s)
    ORDER BY score DESC
    LIMIT 10
    """,(search_term,))
    res = cursor.fetchall()
    res = list(map(lambda x: {
        "id":    x[0],
        "score": x[1],
        "body":  x[2]
    }, res))
    return res


def get_question_details(id):
    cursor = app.conn.cursor()
    cursor.execute("""
    SELECT id, score, accepted_answer, body
    FROM public.question 
    WHERE id=%s;""", (id,))
    
    res = cursor.fetchone()
    res = {
        "id":           res[0],
        "score":        res[1],
        "answer_id":    res[2],
        "body":         res[3]
    }
    return res


def get_answers_for_question(question_id):
    cursor = app.conn.cursor()
    cursor.execute(""" 
            SELECT question.id, answer.id, answer.score, answer.body 
            FROM question JOIN answer ON (question.id = answer.question_id)
            WHERE question.id=%s
            ORDER BY answer.score DESC 
            """, (question_id,))
    res = cursor.fetchall()
    res = list(map(lambda x: {
        "question_id":  x[0],
        "answer_id":    x[1],
        "answer_score": x[2],
        "answer_body":  x[3]
    }, res))
    return res
