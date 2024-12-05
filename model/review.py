from model.db_connection import db_connection
from model.review_state import DraftState, PublishedState

class Review:
    #review object initialization
    def __init__(self, review_id, user_id, rname, rating, description,
                 address, state, timestamp):
        self.review_id = review_id
        self.user_id = user_id
        self.rname = rname
        self.rating = rating
        self.description = description
        self.address = address
        self.state = self.state_from_string(state)
        self.timestamp = timestamp

    #used to help with database conversion from a string to the ReviewState
    @staticmethod
    def state_from_string(state_string):
        if state_string == 'draft':
            return DraftState()
        elif state_string == 'published':
            return PublishedState()

    #used to help convert ReviewState to string to store in database
    def string_from_state(self):
        if isinstance(self.state, DraftState):
            return 'draft'
        elif isinstance(self.state, PublishedState):
            return 'published'

    #calls upon the DraftState or PublishedState publish()/draft() method when a Review object's
    #state is set to either. if state matches method, no change, if they are not matching,
    #the state is updated
    def publish(self):
        self.state.publish(self)

    def draft(self):
        self.state.draft(self)

    #insert review into the database
    def insert_review(self):
        conn = db_connection()
        cursor = conn.cursor()
        #convert the ReviewState into a string to store in the database
        state_str = self.string_from_state()
        cursor.execute(
            "INSERT INTO reviews (user_id, rname, rating, description, address, state, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (self.user_id, self.rname, self.rating, self.description,
             self.address, state_str, self.timestamp)
        )
        conn.commit()
        conn.close()

    #get review from database by id and return review object
    @staticmethod
    def get_review(review_id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reviews WHERE review_id = ?", (review_id)
        )
        review = cursor.fetchone()
        conn.close()
        return Review(review_id=review[0], user_id=review[1],
                      rname=review[2], rating=review[3],
                      description=review[4], address=review[5],
                      state=review[6], timestamp=review[7])

    #get all reviews from the database by user id and return list of reviews
    @staticmethod
    def get_all_reviews_by_user(user_id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reviews WHERE user_id = ?", (user_id)
        )
        reviews = cursor.fetchall()
        conn.close()
        return [
            {
                "review_id": row[0],
                "user_id": row[1],
                "rname": row[2],
                "rating": row[3],
                "description": row[4],
                "address": row[5],
                "state": row[6],
                "timestamp": row[7]
            }
            for row in reviews
        ]

    #get all reviews from the database where state is published, and return a
    #list of reviews and their associated usernames
    @staticmethod
    def get_all_published_reviews():
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT a.*, b.username FROM reviews a INNER JOIN users b on a.user_id = b.user_id"
            " where a.state = 'published'"
            "order by a.timestamp desc"
        )
        reviews = cursor.fetchall()
        conn.close()
        return [
            {
                "review_id": row[0],
                "user_id": row[1],
                "rname": row[2],
                "rating": row[3],
                "description": row[4],
                "address": row[5],
                "state": row[6],
                "timestamp": row[7],
                "username": row[8]
            }
            for row in reviews
        ]

    #update review in the database
    def update_review(self):
        conn = db_connection()
        cursor = conn.cursor()
        # convert the ReviewState into a string to store in the database
        state_str = self.string_from_state()
        cursor.execute(
            "UPDATE reviews SET rname = ?, rating = ?, description = ?, address = ?, state = ?, timestamp = ? WHERE review_id = ?",
            (self.rname, self.rating, self.description, self.address,
             state_str, self.timestamp, self.review_id)
        )
        conn.commit()
        conn.close()

    #delete review from database
    def delete_review(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM reviews WHERE review_id = ?", (self.review_id)
        )
        conn.commit()
        conn.close()
