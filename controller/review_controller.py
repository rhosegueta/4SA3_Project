from datetime import datetime

from model.review import Review
from model.review_factory import ReviewFactory
from model.review_state import DraftState, PublishedState


class ReviewController:
    #method to create review, takes attributes from view/app
    #passes those through to the ReviewFactory class which helps
    #to create Review objects with default settings
    #inserts created Review object into database
    @staticmethod
    def create_review(user_id, rname, rating, description, address):
        review = ReviewFactory.create_review(user_id, rname, rating, description, address)
        review.insert_review()

    #gets review by id
    @staticmethod
    def get_review(review_id):
        return Review.get_review(review_id)

    #gets list of reviews by user id
    @staticmethod
    def get_all_reviews_by_user(user_id):
        return Review.get_all_reviews_by_user(user_id)

    #gets all reviews with PublishedState state
    @staticmethod
    def get_all_published_reviews():
        return Review.get_all_published_reviews()

    #method to update review
    @staticmethod
    def update_review(review_id, rname, rating, description, address, state):
        review = Review.get_review(review_id)
        review.rname = rname
        review.rating = rating
        #appends the time edited to the description
        review.description = description + '<br>Edited on: ' + str(datetime.now())
        review.address = address
        review.timestamp = datetime.now()

        #state is passed as a string through a form
        #to maintain use of the State design pattern, this method checks
        #what the current state of the object is and if it is
        #a different state from what has been selected,
        #it uses the publish() or draft() method to update it
        if state == 'published' and isinstance(review.state, DraftState):
            review.publish()
        elif state == 'draft' and isinstance(review.state, PublishedState):
            review.draft()
        review.update_review()

    #deletes review by id
    @staticmethod
    def delete_review(review_id):
        review = Review.get_review(review_id)
        review.delete_review()