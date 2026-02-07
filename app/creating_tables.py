def create_tables(con, cursor):
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
    cursor.execute(
        """
            CREATE TABLE if not exists user_token (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL UNIQUE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP WITH TIME ZONE NOT NULL
            );
        """
    )
    con.commit()