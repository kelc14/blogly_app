"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
    
    def delete_user(self):
        """Delete the user."""
        User.query.filter_by(id=self.id).delete()
        db.session.commit()
        return
    
    @property
    def full_name(self):
        """The full name property"""
        return f"{self.first_name} {self.last_name}"

    