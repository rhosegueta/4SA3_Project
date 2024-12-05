#table structures
from model.db_connection import db_connection

conn = db_connection()
cursor = conn.cursor()

try:
    cursor.execute("""
        CREATE TABLE Users (
            user_id int NOT NULL PRIMARY KEY IDENTITY,
            fname varchar(255),
            lname varchar(255),
            username varchar(255),
            password varchar(255)
        );
    """)
    conn.commit()
except Exception as e:
    #Table exists already
    print(e)

#if user is deleted, delete all associated reviews
try:
    cursor.execute("""
        CREATE TABLE Reviews (
            review_id int NOT NULL PRIMARY KEY IDENTITY,
            user_id int NOT NULL,
            rname varchar(255),
            rating int,
            description varchar(255),
            address varchar(255),
            state varchar(255),
            timestamp datetime,
            constraint FK_Reviews_Users FOREIGN KEY (user_id) 
            REFERENCES Users (user_id) ON DELETE CASCADE
        );
    """)
    conn.commit()
except Exception as e:
    print(e)

#if review is deleted, delete all associated comments
#if a user is deleted, it will delete all their reviews and
#when the review is deleted all comments will also be deleted
try:
    cursor.execute("""
        CREATE TABLE Comments (
            comment_id int NOT NULL PRIMARY KEY IDENTITY,
            review_id int NOT NULL,
            user_id int NOT NULL,
            content varchar(255),
            timestamp datetime,
            constraint FK_Comments_Reviews FOREIGN KEY (review_id) 
            REFERENCES Reviews (review_id) ON DELETE CASCADE,
            constraint FK_Comments_Users FOREIGN KEY (user_id) 
            REFERENCES Users (user_id) ON DELETE NO ACTION
        );
    """)
    conn.commit()
except Exception as e:
    print(e)