import psycopg2

conn = psycopg2.connect(host="db", database="stackoverflow", user="postgres", password="stackoverflow")

print(conn)