from models import User, db
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