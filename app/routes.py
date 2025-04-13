# app/routes.py

from flask import Blueprint, request, jsonify
from app.models import db, Guest, Episode, Appearance

bp = Blueprint('api', __name__)

# GET /episodes
# app/routes.py
@bp.route('/episodes', methods=['GET'])
def get_episodes():
    try:
        episodes = Episode.query.all()

        if not episodes:
            return jsonify({"error": "No episodes found"}), 404

        result = []
        for e in episodes:
            episode_data = {
                "id": e.id,
                "date": e.date,
                "guests": []
            }

            for a in e.appearances:
                guest = a.guest  # Get the associated guest

                if guest is not None:  # Check if the guest exists
                    episode_data["guests"].append({
                        "id": guest.id,
                        "name": guest.name,
                        "rating": a.rating
                    })
                else:
                    # In case of invalid guest_id, log an error or handle gracefully
                    episode_data["guests"].append({
                        "error": "Guest not found",
                        "rating": a.rating
                    })

            result.append(episode_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

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

    # Validation: all fields present
    if rating is None or guest_id is None or episode_id is None:
        return jsonify({"error": "Missing data"}), 400

    # Validation: rating is int between 1 and 5
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be an integer between 1 and 5"}), 400

    # Validation: guest and episode must exist
    guest = Guest.query.get(guest_id)
    episode = Episode.query.get(episode_id)

    if guest is None or episode is None:
        return jsonify({"error": "Invalid guest_id or episode_id"}), 400

    # Create appearance
    appearance = Appearance(
        rating=rating,
        guest_id=guest_id,
        episode_id=episode_id
    )

    db.session.add(appearance)
    db.session.commit()

    return jsonify(appearance.to_dict()), 201
