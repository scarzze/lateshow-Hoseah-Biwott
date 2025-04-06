# seed.py
import datetime
from app import create_app, db
from app.models import Guest, Episode, Appearance

# Create Flask app and connect to DB
app = create_app()

# Sample data from your raw list
raw_data = [
    ("1999", "actor", "1/11/99", "Acting", "Michael J. Fox"),
    ("1999", "Comedian", "1/12/99", "Comedy", "Sandra Bernhard"),
    ("1999", "television actress", "1/13/99", "Acting", "Tracey Ullman"),
    # Add all the other data here...
]

with app.app_context():
    # Clear the tables (Optional, can be commented out if data already exists)
    db.drop_all()
    db.create_all()

    # Add guests and episodes
    for year, occupation, date_str, group, name in raw_data:
        date = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
        
        # Create new guest
        guest = Guest(name=name, occupation=occupation, group=group)
        db.session.add(guest)
        
        # Create new episode
        episode = Episode(date=date)
        db.session.add(episode)
        
        # Commit to DB
        db.session.commit()

        # Create appearance with a random rating (1 to 5, just for seed purposes)
        appearance = Appearance(rating=5, guest_id=guest.id, episode_id=episode.id)
        db.session.add(appearance)

    # Commit all data at once
    db.session.commit()

    print("Seeding complete!")
