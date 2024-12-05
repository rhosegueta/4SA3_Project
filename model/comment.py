from model.db_connection import db_connection

class Comment:
    #comment initialization
    def __init__(self, comment_id, review_id, user_id,
                 content, timestamp):
        self.comment_id = comment_id
        self.review_id = review_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp

    #inserts comment into the database
    def insert_comment(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (review_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)",
            (self. review_id, self.user_id, self.content, self.timestamp)
        )
        conn.commit()
        conn.close()

    #gets comment by id from database and returns comment object
    @staticmethod
    def get_comment(comment_id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM comments WHERE comment_id = ?", (comment_id)
        )
        comment = cursor.fetchone()
        conn.close()
        print(comment)
        return Comment(comment_id=comment[0], review_id=comment[1],
                       user_id=comment[2], content=comment[3], timestamp=comment[4])

    #gets all comments by review id from the database and returns list of
    #comments and associated usernames
    @staticmethod
    def get_all_comments_by_review(review_id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT a.*, b.username FROM comments a
            inner join users b on a.user_id = b.user_id WHERE a.review_id = ?
            order by a.timestamp asc""", (review_id)
        )
        comments = cursor.fetchall()
        conn.close()
        return [
            {
                "comment_id": row[0],
                "review_id": row[1],
                "user_id": row[2],
                "content": row[3],
                "timestamp": row[4],
                "username": row[5]
            }
            for row in comments
        ]

    #updates comment in database
    def update_comment(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE comments SET content = ?, timestamp = ? WHERE comment_id = ?",
            (self.content, self.timestamp, self.comment_id)
        )
        conn.commit()
        conn.close()

    #deletes comment from database
    def delete_comment(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM comments WHERE comment_id = ?", (self.comment_id)
        )
        conn.commit()
        conn.close()