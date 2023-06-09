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

    def __repr__ (self):
         e = self
         return f"<User {e.id}, full_name = {e.full_name}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50), 
                           nullable=False)
    last_name = db.Column(db.String(50), 
                           nullable=False)
    image_url = db.Column(db.Text,
                          default = 'https://www.nicepng.com/png/detail/73-730154_open-default-profile-picture-png.png')
    
    posts = db.relationship('Post', backref="user", cascade='all,delete')
    
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

    def __repr__ (self):
         e = self
         return f"<Post {e.id}, title = {e.title}, user_id={e.user_id}>"

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
    
    tags = db.relationship('Tag', secondary="posts_tags", backref="posts", cascade="save-update")

    
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
        


class Tag(db.Model):
        """Model for tags in Blogly"""

        __tablename__ = 'tags'

        def __repr__ (self):
         e = self
         return f"<tag_id {e.id}, name = {e.name}>"

        id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
        
        name = db.Column(db.String(50), 
                           nullable=False,
                            unique=True)
        
        def delete_tag(self):
            """Delete the tag."""
            tag = Tag.query.filter_by(id=self.id).first()
            db.session.delete(tag)
            db.session.commit()
            return
        
class PostTag(db.Model):
        """Mapping for tags onto posts in Blogly"""

        __tablename__ = 'posts_tags'

        def __repr__ (self):
         e = self
         return f"<post_id {e.post_id}, tag_id = {e.tag_id}>"
        
        post_id = db.Column(db.Integer,
                           db.ForeignKey('posts.id'),
                           primary_key=True)
        tag_id = db.Column(db.Integer,
                           db.ForeignKey('tags.id'),
                           primary_key=True)
        
        def remove_tag_from_post(self):
            """Remove the tag from the post."""
            post_tag = PostTag.query.filter_by(post_id=self.post_id, tag_id=self.tag_id).first()
            db.session.delete(post_tag)
            db.session.commit()
            return

    