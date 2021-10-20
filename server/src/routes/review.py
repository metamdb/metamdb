"""Routes for testing."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from src.models.casm import ReactionHistory, ReactionHistorySchema

from src.errors import handler
from src import db

review_blueprint = Blueprint('review', __name__, url_prefix='/api/review')

APPROVED_REVIEWERS = [2, 3]


@review_blueprint.route('', methods=['POST'])
@jwt_required()
def review():
    reviews = request.get_json()
    if not reviews:
        raise handler.InvalidReviews()

    history_schema = ReactionHistorySchema(many=True)

    if current_user.role_id in APPROVED_REVIEWERS:
        for review in reviews:
            if review['approved'] is not None:
                reaction_history = ReactionHistory.query.get(review['id'])

                if review['approved']:
                    ReactionHistory.update_reaction(reaction_history)
                    reaction_history.review_status_id = 2

                elif not review['approved']:
                    reaction_history.review_status_id = 3

                reaction_history.reviewed_by_id = current_user.id

                db.session.add(reaction_history)
                db.session.commit()

        review = ReactionHistory.query.filter(
            ReactionHistory.review_status_id == 1).all()
        review_dump = history_schema.dump(review)
    else:
        review_dump = None

    return jsonify({'reviews': review_dump})