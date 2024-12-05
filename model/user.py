from model.db_connection import db_connection

class User:
    #initialize user object
    def __init__(self, user_id, username, password, fname, lname):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname

    #insert user into database
    def insert_user(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, fname, lname) VALUES (?, ?, ?, ?)",
            (self.username, self.password, self.fname, self.lname)
        )
        conn.commit()
        conn.close()

    #get user from database, return user object
    @staticmethod
    def get_user(user_id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id)
        )
        user = cursor.fetchone()
        conn.close()
        return User(user_id=user[0],username=user[3],password=user[4],
                    fname=user[1],lname=user[2])

    #get user from database, return user object
    @staticmethod
    def get_user_by_username(username):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username)
        )
        user = cursor.fetchone()
        conn.close()
        return User(user_id=user[0],username=user[3],password=user[4],
                    fname=user[1],lname=user[2])

    #update user in database
    def update_user(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, password = ?, fname = ?, lname = ? WHERE user_id = ?",
            (self.username, self.password, self.fname, self.lname, self.user_id)
        )
        conn.commit()
        conn.close()

    #delete user from database
    def delete_user(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM users WHERE user_id = ?",
            (self.user_id)
        )
        conn.commit()
        conn.close()