"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Model for user database and methods. """

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50), 
                           nullable=False)
    last_name = db.Column(db.String(50), 
                           nullable=False)
    image_url = db.Column(db.Text,
                          default = 'https://www.nicepng.com/png/detail/73-730154_open-default-profile-picture-png.png')
    
    # posts = db.relationship('Post', backref="user", lazy=True, cascade='all,delete')
    
    def delete_user(self):
        """Delete the user."""
        user = User.query.filter_by(id=self.id).first()
        db.session.delete(user)
        db.session.commit()
        return
    
    @property
    def full_name(self):
        """The full name property"""
        return f"{self.first_name} {self.last_name}"
    


class Post(db.Model):
    """Model for user posts"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50), 
                      nullable=False)
    content = db.Column(db.Text, 
                        nullable=False)
    created_at = db.Column(db.Text, 
                           default=f"{datetime.now()}")
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref=backref("posts", cascade="all,delete"))


    def delete_post(self):
        """Delete the post."""
        post = Post.query.filter_by(id=self.id).first()
        db.session.delete(post)
        db.session.commit()
        return
    
    def display_date_time(self):
        current_date = self.created_at
        date_time = str(current_date).split('.')[0]
        date_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = months[date_obj.month - 1]

        return f"{month} {date_obj.day}, {date_obj.year} at {date_obj.hour}:{date_obj.minute}"
        

    