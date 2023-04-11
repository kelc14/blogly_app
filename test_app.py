from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# db.drop_all()
# db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """FIRST CLEAR DB, then add sample user and post"""
        # User.query.delete()
        # db.session.close()
        db.drop_all()
        db.create_all()

        # CREATE SAMPLE USER
        user= User(first_name="Jane", last_name="Smith", image_url="https://us.123rf.com/450wm/fizkes/fizkes2011/fizkes201102042/159430998-headshot-portrait-profile-picture-of-pretty-smiling-young-woman-posing-indoors-looking-at-camera.jpg?ver=6")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        # CREATE SAMPLE POST (WRITTEN BY SAMPLE USER)
        post = Post(title="Hello", content='This is the content.', user_id=self.user_id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

        # CREATE SAMPLE TAG
        tag = Tag(name="blogger")

        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

        # ASSOCIATE SAMPLE TAG WITH SAMPLE POST
        post_tag = PostTag(post_id=self.post_id,tag_id=self.tag_id)
        db.session.add(post_tag)
        db.session.commit()

    
    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()
    
    def test_show_homepage(self):
        """Test that the recent posts appear when viewing the homepage"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)
            # check that our test case appears
            self.assertIn('<h5 class="card-title">Hello</h5>', html)
            # check that the tag appears with the post 
            self.assertIn('<small class="p-1"><i>blogger</i></small>', html)

    #############################################################################################################
    
    #### tests for users 

    def test_list_users(self):
        """Test that our test user is displayed in the list of users."""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane', html)

    def test_show_user_profile(self):
        """Test that our test user's full name is displayed on the user profile. """
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-2 text-center">Jane Smith</h2>', html)
            # check that the sample post title appears on the page
            self.assertIn(f'<a href="/posts/{self.post_id}">Hello</a>', html)

    def test_user_update(self):
        """Test that when we edit user information, a redirect occurs"""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/edit', data={
                "first_name": 'Purple',
                "last_name": 'Moon',
                "image_url": "https://us.123rf.com/450wm/fizkes/fizkes2011/fizkes201102042/159430998-headshot-portrait-profile-picture-of-pretty-smiling-young-woman-posing-indoors-looking-at-camera.jpg?ver=6"
            })

            self.assertEqual(resp.status_code, 302)

    def test_user_update_redirect(self):
        """Follow the redirect and test that our new user name is displayed in the user profiled details."""
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
        """Test that when we delete a user via post request, a redirect occurs"""
        with app.test_client() as client:
            resp  = client.post(f'/users/{self.user_id}/delete')
            
            self.assertEqual(resp.status_code, 302)

    def test_delete_redirect(self):
        """Test that after the post request occurs for delete user, that the user is NOT displayed on the user list"""
        with app.test_client() as client:
            resp  = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Jane Smith', html)


    #############################################################################################################

    ######  tests for posts

    def test_display_new_post_form(self):
        """Check that the display new post form is customized for the user with user_id"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-4 text-center">Create a New Post for Jane Smith</h2>', html)
            # test that our tags appear on our new post form
            self.assertIn(f'<input type="checkbox" name="tag" value="{self.tag_id}" />', html)

    def test_submit_new_post(self):
        """Test that when a post request occurs for creating a new post, a redirect occurs"""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new', data={
                "title": "Did you know... Zebra Edition",
                "content": "ZEBRAS STRIPES ARE UNIQUE LIKE FINGERPRINTS! Their black and white stripes are unique and are as distinctive as human fingerprints. When a foal is born, they have reddish-brown stripes which gradually become darker and change to black as they grow.",
                "user_id": self.user_id
            })
            # test that redirect occurs when a new post is submitted
            self.assertEqual(resp.status_code, 302)
    
    def test_new_post_redirect(self):
        """Follow the redirect from creating a new post, and test that the new post is displayed.  Test that our flash message also appears."""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new',  data={
                "title": "Did you know... Zebra Edition",
                "content": "ZEBRAS STRIPES ARE UNIQUE LIKE FINGERPRINTS! Their black and white stripes are unique and are as distinctive as human fingerprints. When a foal is born, they have reddish-brown stripes which gradually become darker and change to black as they grow.",
                "user_id": self.user_id
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # test that the flash message appeared
            self.assertIn('New Post Added!',html)
            # test that the new post title is displayed on the homepage
            self.assertIn('Did you know... Zebra Edition', html)
            

    def test_view_post(self):
        """Test that the post information is displayed"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # test that the post title displays 
            self.assertIn('<h2 class="display-3 mt-5">Hello</h2>', html)

    def test_edit_post_form_display(self):
        """Test that the edit post form is customized with the post information in the value attribute"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input\n        type="text"\n        name="title"\n        value="Hello"\n        class="form-control"\n      />',html)

    def test_edit_post_form_submit(self):
        """Test that when a post request occurs when submitting edit post form, that redirect occurs"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit', data={
                "title": "Hello Version 2",
                "content": "This is just another blog post for you to read.",
                "user_id": self.user_id
            })

            self.assertEqual(resp.status_code, 302)

    def test_edit_post_form_submit_redirect(self):
        """Follow the edit post redirect, and check that the new post title appears in the post detail page."""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit', data={
                "title": "Hello Version 2",
                "content": "This is just another blog post for you to read.",
                "user_id": self.user_id
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-3 mt-5">Hello Version 2</h2>', html)

    def test_delete_post(self):
        """Test that when we execute post request to delete the post, the redirect occurs"""
        with app.test_client() as client:
            resp  = client.post(f'/posts/{self.post_id}/delete')
            
            self.assertEqual(resp.status_code, 302)

    def test_delete_post_redirect(self):
        """Follow the redirect from deleting post and test that the post no longer appears"""
        with app.test_client() as client:
            resp  = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Hello', html)

    

    #############################################################################################################

    ######  tests for tags


    def test_view_tags(self):
        """Test that route works for displaying tags.  Test that our sample tag appears on the page. """
        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            # check that our sample case is displayed
            self.assertIn('blogger', html)

    def test_tag_detail_view(self):
        """Test that the tag detail page loads properly, and that sample post associated with the tag appears in the list"""
        with app.test_client() as client:
            resp = client.get(f'/tags/{self.tag_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # check that the post with tag_id appears in our detail page
            self.assertIn('<h5 class="card-title">Hello</h5>', html)

    def test_edit_tag_display(self):
        """Test that the edit tag form is customized with the tag information in the value attribute"""
        with app.test_client() as client:
            resp = client.get(f'/tags/{self.tag_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input\n        type="text"\n        name="name"\n        value="blogger"\n        class="form-control"\n      />', html)
            
    def test_edit_post_form_submit(self):
        """Test that when a post request occurs when submitting edit post form, that redirect occurs"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit', data={
                "title": "Hello Version 2",
                "content": "This is just another blog post for you to read.",
                "user_id": self.user_id
            })

            self.assertEqual(resp.status_code, 302)

    def test_edit_tag_form_submit_redirect(self):
        """Follow the edit tag redirect, and check that the new tag appears in the tag detail page."""
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag_id}/edit', data={
                "name": "funny"
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-2 text-center">#funny</h2>', html)

    def test_delete_tag(self):
        """Test that when we execute post request to delete the tag, the redirect occurs"""
        with app.test_client() as client:
            resp  = client.post(f'/tags/{self.tag_id}/delete')
            
            self.assertEqual(resp.status_code, 302)

    def test_delete_tag_redirect(self):
        """Follow the redirect from deleting tag and test that the tag no longer appears"""
        with app.test_client() as client:
            resp  = client.post(f'/tags/{self.tag_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('blogger', html)
