import psycopg2


connection_string = {
    'host': '127.0.0.1',
    'user': 'postgres',
    'password': 'stackoverflow',
    'database': 'stackoverflow',
    'port': 5432
}

conn = psycopg2.connect(host=connection_string['host'], database=connection_string['database'], port=connection_string['port'],
    user=connection_string['user'], password=connection_string['password'])
cursor = conn.cursor()
cursor.execute(
            """ SELECT score, body FROM public.question LIMIT 10;""")
 
for r in cursor:
    print(r)