"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add user
callahan = User(first_name='Callahan', last_name="Cowley",
                image_url="https://images.app.goo.gl/4iqKfJVskyGb4Pps7")
courtney = User(first_name='Courtney', last_name="Cowley")


# Add new objects to session, so they'll persist
db.session.add(callahan)
db.session.add(courtney)

# Commit--otherwise, this never gets saved!
db.session.commit()
