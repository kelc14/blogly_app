"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'secret123!'
debug = DebugToolbarExtension(app)


@app.route('/')
def show_home():
    """Redirect to list of users."""
    return redirect("/users")
    

@app.route('/users')
def display_users():
    """Display all users"""
    users = User.query.order_by(User.last_name).order_by(User.first_name).all()
    return render_template('home.html', users=users)

@app.route('/users/new')
def display_add_user():
    """Display new user form"""
    return render_template('add_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """"Add new user and redirect to user page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] 
    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route('/users/<int:user_id>')
def display_user(user_id):
    """Display the profile page for the specified user."""
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def display_edit_user(user_id):
    """Display page to edit user information."""
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update user information in db"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user from the db"""
    user = User.query.get(user_id)
    user.delete_user()
    return redirect('/users')
