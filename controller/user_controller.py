from flask import session
from model.user import User

class UserController:
    #creates User object from attributes received from view/app
    #inserts into database
    @staticmethod
    def create_user(username, password, fname, lname):
        user = User(user_id=None, username=username,
                    password=password, fname=fname, lname=lname)
        user.insert_user()

    #gets user by id
    @staticmethod
    def get_user(user_id):
        return User.get_user(user_id)

    #updates user
    @staticmethod
    def update_user(user_id, username, password, fname, lname):
        user = User.get_user(user_id)
        user.username = username
        user.password = password
        user.fname = fname
        user.lname = lname
        user.update_user()

    #deletes user by id
    @staticmethod
    def delete_user(user_id):
        user = User.get_user(user_id)
        user.delete_user()

    #"logs" in user by checking if a user with the entered username exists
    #and if the password entered matches the one in the database
    #stores the user id in the session
    @staticmethod
    def login(username, password):

        user = User.get_user_by_username(username)

        if user and user.password == password:
            session['user_id'] = user.user_id
            return user
        return None

    #logs out user by removing the user id from the session
    @staticmethod
    def logout():
        session.pop('user_id', None)

