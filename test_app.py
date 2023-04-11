from unittest import TestCase

from app import app
from models import db, User, Post 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user"""
        User.query.delete()

        user= User(first_name="Jane", last_name="Smith", image_url="https://us.123rf.com/450wm/fizkes/fizkes2011/fizkes201102042/159430998-headshot-portrait-profile-picture-of-pretty-smiling-young-woman-posing-indoors-looking-at-camera.jpg?ver=6")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        # post = Post(title="Hello", content='This is the content.', user_id=self.user_id)

        # db.session.add(post)
        # db.session.commit()
    
    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()
    
    def test_show_homepage(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)

    #### tests for users 
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane', html)

    def test_show_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-2 text-center">Jane Smith</h2>', html)

    def test_user_update(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/edit', data={
                "first_name": 'Purple',
                "last_name": 'Moon',
                "image_url": "https://us.123rf.com/450wm/fizkes/fizkes2011/fizkes201102042/159430998-headshot-portrait-profile-picture-of-pretty-smiling-young-woman-posing-indoors-looking-at-camera.jpg?ver=6"
            })

            self.assertEqual(resp.status_code, 302)

    def test_user_update_redirect(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/edit', data={
                    "first_name": 'Purple',
                    "last_name": 'Moon',
                    "image_url": "https://us.123rf.com/450wm/fizkes/fizkes2011/fizkes201102042/159430998-headshot-portrait-profile-picture-of-pretty-smiling-young-woman-posing-indoors-looking-at-camera.jpg?ver=6"
                }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Purple Moon', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp  = client.post(f'/users/{self.user_id}/delete')
            
            self.assertEqual(resp.status_code, 302)

    def test_delete_redirect(self):
        with app.test_client() as client:
            resp  = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Jane Smith', html)


    ######  tests for posts
