from . import db

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String)
    group = db.Column(db.String)

    appearances = db.relationship('Appearance', back_populates='guest', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation,
            "group": self.group,
            "appearances": [
                {
                    "id": a.id,
                    "rating": a.rating,
                    "episode": {
                        "id": a.episode.id,
                        "date": a.episode.date
                    }
                }
                for a in self.appearances
            ]
        }

class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)

    appearances = db.relationship('Appearance', back_populates='episode', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "guests": [
                {
                    "id": a.guest.id,
                    "name": a.guest.name,
                    "rating": a.rating
                }
                for a in self.appearances
            ]
        }

class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)

    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "guest": {
                "id": self.guest.id,
                "name": self.guest.name
            },
            "episode": {
                "id": self.episode.id,
                "date": self.episode.date
            }
        }
