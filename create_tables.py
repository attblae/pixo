def users_base(con, cursor):
    cursor.execute(
    """
        CREATE TABLE if not exists users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(30) UNIQUE,
            password VARCHAR(255),
            name VARCHAR(35),
            surname VARCHAR(35),
            patronymic VARCHAR(35),
            phone VARCHAR(11) UNIQUE,
            email VARCHAR(50),
            passport_number VARCHAR(16) UNIQUE,
            card VARCHAR(19) UNIQUE
        );
    """
    )
    con.commit()



