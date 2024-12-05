from datetime import datetime
from model.comment import Comment

class CommentController:
    #method to create comment object, takes attributes passed from the view/app
    #uses current time as the timestamp
    #uses comment method insert_comment to insert into the database
    @staticmethod
    def create_comment(review_id, user_id, content):
        comment = Comment(comment_id=None, review_id=review_id,
                          user_id=user_id, content=content,
                          timestamp=datetime.now())
        comment.insert_comment()

    #gets comment object by id
    @staticmethod
    def get_comment(comment_id):
        return Comment.get_comment(comment_id)

    #gets list of comment objects by review id
    @staticmethod
    def get_all_comments_by_review(review_id):
        return Comment.get_all_comments_by_review(review_id)

    #updates comment object
    @staticmethod
    def update_comment(comment_id, content):
        comment = Comment.get_comment(comment_id)
        #appends timestamp and updated comment to the original comment
        #for tracking purposes so others know when the comment has been edited
        og_content = comment.content
        comment.content = og_content + '<br>Edited @ ' + str(datetime.now()) + ': ' + content

        comment.update_comment()

    #deleted comment by id
    @staticmethod
    def delete_comment(comment_id):
        comment = Comment.get_comment(comment_id)
        comment.delete_comment()
