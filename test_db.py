from db_helper import get_db

db = get_db()
cur = db.cursor()
cur.execute("SELECT NOW();")
print(cur.fetchone())
db.close()
