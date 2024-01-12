import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM clinic")
cursor.execute()

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()