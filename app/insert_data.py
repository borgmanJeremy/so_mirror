import psycopg2
import psycopg2.extras
from lxml import etree

connection_string = {
    'host': '127.0.0.1',
    'user': 'postgres',
    'password': 'stackoverflow',
    'database': 'stackoverflow',
    'port': 5432
}


def provision_database(conn_string):

    conn = psycopg2.connect(host=conn_string['host'], port=conn_string['port'],
                            user=conn_string['user'], password=conn_string['password'])
    conn.autocommit = True

    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE DATABASE stackoverflow;''')
    except:
        print("Database Already exists")
    conn.close()

    conn = psycopg2.connect(host=conn_string['host'], database=conn_string['database'], port=conn_string['port'],
                            user=conn_string['user'], password=conn_string['password'])

    conn.autocommit = True
    cursor = conn.cursor()

    # Create Schema
    cursor.execute(open("./db/create.sql", "r").read())

    # Populate Question Types
    try:
        cursor.execute(
            """INSERT INTO public.post_type (id, description) VALUES (%s, %s);""", (1, "Question"))
    except:
        print("Already inserted")

    try:
        cursor.execute(
            """INSERT INTO public.post_type (id, description) VALUES (%s, %s);""", (2, "Answer"))
    except:
        print("Already Inserted")

    conn.close()


# Iterator that returns question
class QuestionIterator:
    def __init__(self, xml_iter):
        self.xml_iter = xml_iter

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            (_event, child) = next(self.xml_iter)
            if child.attrib['PostTypeId'] == '1':
                accepted_answer = child.attrib['AcceptedAnswerId'] if 'AcceptedAnswerId' in child.attrib else None
                question = (child.attrib['Id'],
                            child.attrib['PostTypeId'],
                            child.attrib['Score'],
                            accepted_answer,
                            child.attrib['CreationDate'],
                            child.attrib['Body'])

                child.clear(keep_tail=True)
                return question
            child.clear(keep_tail=True)


class AnswerIterator:
    def __init__(self, xml_iter):
        self.xml_iter = xml_iter

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            (_event, child) = next(self.xml_iter)
            if child.attrib['PostTypeId'] == '2':
                answer_list = (child.attrib['Id'],
                               child.attrib['PostTypeId'],
                               child.attrib['Score'],
                               child.attrib['ParentId'],
                               child.attrib['CreationDate'],
                               child.attrib['Body'])

                child.clear(keep_tail=True)
                return answer_list
            child.clear(keep_tail=True)


def batch_insert(conn, sql, iter):
    cursor = conn.cursor()
    psycopg2.extras.execute_batch(cursor, sql, iter, page_size=1000)
    cursor.close()


def insert_question(conn, question):
    batch_insert(conn, """
        INSERT INTO public.question
          (id, post_type, score, accepted_answer, created_date, body) 
        VALUES 
          (%s, %s, %s, %s, %s, %s);
        """, question)


def insert_answer(conn, answer):
    batch_insert(conn, """
        INSERT INTO public.answer
          (id, post_type, score, question_id, created_date, body) 
        VALUES 
          (%s, %s, %s, %s, %s, %s);
        """, answer)


def add_indexes(conn):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE INDEX idx_question_id ON public.answer(question_id); ")
    cursor.execute("""
        ALTER TABLE public.question ADD COLUMN ts tsvector 
        GENERATED ALWAYS AS (to_tsvector('english', body)) STORED;""")
    cursor.execute(
        """CREATE INDEX ts_idx ON public.question USING GIN (ts);""")
    cursor.close()


if __name__ == '__main__':
    provision_database(connection_string)

    conn = psycopg2.connect(host=connection_string['host'], port=connection_string['port'], database=connection_string['database'],
                            user=connection_string['user'], password=connection_string['password'])

    conn.autocommit = True

    print('Inserting questions')
    xml_iter = etree.iterparse('./data/Posts_small.xml', tag='row')
    question = QuestionIterator(xml_iter)
    insert_question(conn, question)

    xml_iter = etree.iterparse('./data/Posts_small.xml', tag='row')
    answer = AnswerIterator(xml_iter)
    print('Inserting answers')
    insert_answer(conn, answer)

    print('Building Indexes')
    add_indexes(conn)

    print('Done')
