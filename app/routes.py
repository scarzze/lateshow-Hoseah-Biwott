# app/routes.py
from flask import Blueprint, request, jsonify
from app.models import db, Guest, Episode, Appearance

bp = Blueprint('api', __name__)

# GET /episodes
@bp.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([
        {
            "id": e.id,
            "date": e.date,
            "guests": [
                {
                    "id": a.guest.id,
                    "name": a.guest.name,
                    "rating": a.rating
                }
                for a in e.appearances
            ]
        }
        for e in episodes
    ])

# GET /guests
@bp.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([
        {
            "id": g.id,
            "name": g.name,
            "occupation": g.occupation,
            "group": g.group
        } for g in guests
    ])

# GET /episodes/<int:id>
@bp.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get_or_404(id)
    return jsonify({
        "id": episode.id,
        "date": episode.date,
        "guests": [
            {
                "id": a.guest.id,
                "name": a.guest.name,
                "rating": a.rating
            }
            for a in episode.appearances
        ]
    })

# DELETE /episodes/<int:id>
@bp.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get_or_404(id)
    db.session.delete(episode)
    db.session.commit()
    return '', 204

# POST /appearances
@bp.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    rating = data.get("rating")
    guest_id = data.get("guest_id")
    episode_id = data.get("episode_id")

     # Basic data presence check
    if rating is None or guest_id is None or episode_id is None:
        return jsonify({"error": "Missing data"}), 400

    # Rating validation
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be an integer between 1 and 5"}), 400

    # Check existence of guest and episode
    guest = Guest.query.get(guest_id)
    episode = Episode.query.get(episode_id)

    if guest is None or episode is None:
        return jsonify({"error": "Invalid guest_id or episode_id"}), 400

    appearance = Appearance(
        rating=rating,
        guest_id=guest_id,
        episode_id=episode_id
    )
    db.session.add(appearance)
    db.session.commit()

    return jsonify({
        "id": appearance.id,
        "rating": appearance.rating,
        "guest": {
            "id": appearance.guest.id,
            "name": appearance.guest.name
        },
        "episode": {
            "id": appearance.episode.id,
            "date": appearance.episode.date
        }
    }), 201
