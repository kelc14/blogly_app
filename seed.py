from models import User, db, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add users

john = User(first_name="John", last_name="Miller", image_url="https://t4.ftcdn.net/jpg/03/64/21/11/360_F_364211147_1qgLVxv1Tcq0Ohz3FawUfrtONzz8nq3e.jpg")

abby = User(first_name="Abby", last_name="Smith", image_url="https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")

greg = User(first_name="Greg", last_name="Johnson", image_url="https://image.shutterstock.com/mosaic_250/2780032/1770074666/stock-photo-head-shot-of-african-self-assured-executive-manager-portrait-successful-staff-member-company-1770074666.jpg")

db.session.add(john)
db.session.add(abby)
db.session.add(greg)

db.session.commit()

post1 = Post(title="My First Post", content="We went on vacation... I can't wait to tell you all about it. I decided it is time to be a blogger! So here we go!", user_id=2)

post2 = Post(title="My Second Post", content="What's up!!", user_id=2)

post3 = Post(title="Don't call me a blogger yet, but...!", content="My name is greg and I am writing my first blog post. Yay me!", user_id=3)

db.session.add_all([post1, post2, post3])
db.session.commit()


first = Tag(name="first")
funny = Tag(name="funny")
weird = Tag(name="weird")
sunshine = Tag(name="sunshine")
blogger = Tag(name='blogger')

db.session.add_all([first,funny,weird,sunshine, blogger])
db.session.commit()

tag1 = PostTag(post_id=1,tag_id=1)
tag2 = PostTag(post_id=1,tag_id=5)
tag3 = PostTag(post_id=2,tag_id=5)
tag4 = PostTag(post_id=2,tag_id=3)
tag5 = PostTag(post_id=3,tag_id=1)
tag6 = PostTag(post_id=3,tag_id=2)
tag7 = PostTag(post_id=3,tag_id=5)

db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6, tag7])
db.session.commit()
