"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, url_for
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import desc, select


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
    posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    return render_template('home.html', posts=posts)
    

@app.route('/users')
def display_users():
    """Display all users"""
    users = User.query.order_by(User.last_name).order_by(User.first_name).all()
    return render_template('users.html', users=users)

# adding new users

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

    flash('New User Added!')


    return redirect(f"/users/{user.id}")


# display user details, edit user details and delete user

@app.route('/users/<int:user_id>')
def display_user(user_id):
    """Display the profile page for the specified user."""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('users_detail.html', user=user, posts=posts)

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


# add new posts

@app.route('/users/<int:user_id>/posts/new')
def display_new_post_form(user_id):
    """Display a new post form for the user with the given user_id"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('post_new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_user_post(user_id):
    """"Add new user post and redirect to user page"""
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    tag_list = request.form.getlist('tag')
    add_tags = []
    for tag in tag_list:
        post_tag = PostTag(post_id=post.id, tag_id=tag)
        add_tags.append(post_tag)
    db.session.add_all(add_tags)
    db.session.commit()    

    flash('New Post Added!')

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def display_post(post_id):
    """Display the selected post."""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def display_edit_post(post_id):
    """Display the edit form for the selected post."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post_edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Update post information in db"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    posts_tag = PostTag.query.filter_by(post_id=post_id).all()
    for post in posts_tag:
        post.remove_tag_from_post()

    tag_list = request.form.getlist('tag')
    add_tags = []
    for tag in tag_list:
        post_tag = PostTag(post_id=post_id, tag_id=tag)
        add_tags.append(post_tag)
    db.session.add_all(add_tags)
    db.session.commit()  

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a post from the db"""
    post = Post.query.get_or_404(post_id)
    user = post.user_id
    post.delete_post()
    return redirect(f'/users/{user}')

# tags - add, edit, remove

@app.route('/tags')
def display_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def display_tag_info(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/new')
def add_new_tag():
    return render_template('tag_new.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag_to_db():
    """"Add new tag and redirect to tag homepage"""
    name = request.form['name']
    
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    flash('New Tag Added!')

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def display_edit_tag_form(tag_id):
    """Display the edit form for the selected tag."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    """Update tag information in db"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.delete_tag()
    return redirect('/tags')


# if an error is found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
