import sqlite3


con = sqlite3.connect("database.db")
cursor = con.cursor()


cursor.execute(
"""
    CREATE TABLE users if not exists(
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        username VARCHAR(30) UNIQUE,
        password VARCHAR(255) UNIQUE, 
        name VARCHAR(35),
        surname VARCHAR(35),
        patronymic VARCHAR(35),
        phone VARCHAR(11) UNIQUE,
        email VARCHAR(50),
        passport_number(16) UNIQUE,
        card VARCHAR(19) UNIQUE
    );
"""
)



