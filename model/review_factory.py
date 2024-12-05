from datetime import datetime
from model.review import Review

class ReviewFactory:
    #create default review object with draft state (set as text, converted to ReviewState once object is created)
    #and current timestamp
    @staticmethod
    def create_review(user_id, rname, rating, description, address):
        return Review(
            review_id=None,
            user_id=user_id,
            rname=rname,
            rating=rating,
            description=description,
            address=address,
            state='draft',
            timestamp=datetime.now())