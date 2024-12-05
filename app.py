#instructions to run:
#type 'flask run' into the terminal
#may have to install some dependencies like flask and pyodbc

from flask import Flask, render_template, request, redirect, url_for, session
from controller.comment_controller import CommentController
from controller.user_controller import UserController
from controller.review_controller import ReviewController
from config import google_maps_api_key

app = Flask(__name__)
app.secret_key = 'rhose_4sa3_project'

@app.route('/')
def index():
    #if user id is not set (user is not logged in) redirect to login page
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = UserController.get_user(user_id)
    reviews = ReviewController.get_all_published_reviews()
    api_key = google_maps_api_key
    return render_template('index.html', fname=user.fname,
                           reviews=reviews, api_key=api_key)

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    #create user from signup form
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username']
    password = request.form['password']

    UserController.create_user(username, password, fname, lname)

    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    #validate user credentials
    username = request.form['username']
    password = request.form['password']

    user = UserController.login(username, password)

    #if user is validated go to home page, else go back to the login page
    if user:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    UserController.logout()
    return redirect(url_for('login_page'))

@app.route('/user')
def user_page():
    user_id = session.get('user_id')
    user = UserController.get_user(user_id)
    return render_template('user.html', fname=user.fname, lname=user.lname,
                           username=user.username, password_ast=len(user.password)*'*',
                           password=user.password)

@app.route('/update_user', methods=['POST'])
def update_user():
    #update user from form input
    user_id = session.get('user_id')
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username']
    password = request.form['password']
    UserController.update_user(user_id, username, password, fname, lname)
    return redirect(url_for('user_page'))

@app.route('/delete_user')
def delete_user():
    #delete user and remove from session
    user_id = session.get('user_id')
    UserController.delete_user(user_id)
    UserController.logout()
    return redirect(url_for('login_page'))

@app.route('/create_review')
def create_review_page():
    return render_template('create_review.html')

@app.route('/create_review', methods=['POST'])
def create_review():
    #create review from form input
    user_id = session.get('user_id')
    rname = request.form['rname']
    rating = request.form['rating']
    description = request.form['description']
    address = request.form['address']

    ReviewController.create_review(user_id, rname, rating, description, address)

    return redirect(url_for('reviews'))

@app.route('/reviews')
def reviews():
    user_id = session.get('user_id')
    user = UserController.get_user(user_id)

    reviews = ReviewController.get_all_reviews_by_user(user_id)
    api_key = google_maps_api_key

    return render_template('reviews.html', fname=user.fname, reviews=reviews,
                           api_key=api_key)

@app.route('/update_review/<int:review_id>')
def update_review_page(review_id):
    review = ReviewController.get_review(review_id)
    state_str = review.string_from_state()
    api_key = google_maps_api_key
    return render_template('view_review.html',
                           review_id=review_id,
                           rname=review.rname, rating=review.rating,
                           description=review.description, address=review.address,
                           timestamp=review.timestamp, state=state_str,
                           api_key=api_key)

@app.route('/update_review', methods=['POST'])
def update_review():
    #update review from form input
    review_id = request.form['review_id']
    rname = request.form['rname']
    rating = request.form['rating']
    description = request.form['description']
    address = request.form['address']
    state = request.form['state']
    ReviewController.update_review(review_id, rname, rating, description, address, state)

    return redirect(url_for('update_review_page', review_id=review_id))

@app.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    ReviewController.delete_review(review_id)
    return redirect(url_for('reviews'))

@app.route('/view_comments/<int:review_id>')
def view_comments(review_id):
    comments = CommentController.get_all_comments_by_review(review_id)
    review = ReviewController.get_review(review_id)
    state_str = review.string_from_state()
    api_key = google_maps_api_key
    return render_template('view_comments.html',
                           review_id=review_id,
                           rname=review.rname, rating=review.rating,
                           description=review.description, address=review.address,
                           timestamp=review.timestamp, state=state_str,
                           api_key=api_key, comments=comments)

@app.route('/create_comment', methods=['POST'])
def create_comment():
    #create comment from form input
    review_id = request.form['review_id']
    user_id = session.get('user_id')
    content = request.form['content']

    CommentController.create_comment(review_id, user_id, content)
    return redirect(url_for('view_comments', review_id=review_id))

@app.route('/update_comment', methods=['POST'])
def update_comment():
    #update comment from form input
    review_id = request.form['review_id']
    comment_id = request.form['comment_id']
    content = request.form['content']

    CommentController.update_comment(comment_id, content)

    return redirect(url_for('view_comments', review_id=review_id))

@app.route('/delete_comment/<int:review_id>/<int:comment_id>/')
def delete_comment(review_id, comment_id):
    CommentController.delete_comment(comment_id)
    return redirect(url_for('view_comments', review_id=review_id))