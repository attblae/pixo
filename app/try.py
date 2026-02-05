import sqlite3
from create_tables import users_base
con = sqlite3.connect("static/database.db")
cursor = con.cursor()
usernames = cursor.execute('''SELECT username FROM users''').fetchall()
print(usernames)
con.commit()
con.close()