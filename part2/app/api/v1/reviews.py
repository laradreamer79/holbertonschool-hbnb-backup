from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# =========================
# Namespace
# =========================

api = Namespace("reviews", description="Review operations")


# =========================
# Input model
# =========================

review_input = ns.model("ReviewInput", {
    "text": fields.String(required=True, description="Review text"),
    "rating": fields.Integer(required=True, description="Rating (1-5)"),
    "user_id": fields.String(required=True, description="User ID"),
    "place_id": fields.String(required=True, description="Place ID"),
})


# =========================
# Output model
# =========================

review_output = ns.model("ReviewOutput", {
    "id": fields.String,
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
})


# =========================
# Routes
# =========================

@ns.route("/")
class ReviewsCollection(Resource):

    @ns.expect(review_input, validate=True)
    @ns.marshal_with(review_output, code=201)
    def post(self):
        """Create new review"""
        review = facade.create_review(ns.payload or {})
        return review.to_dict(), 201


    @ns.marshal_list_with(review_output, code=200)
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200



@ns.route("/<string:review_id>")
class ReviewItem(Resource):

    @ns.marshal_with(review_output, code=200)
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)

        if not review:
            ns.abort(404, "Review not found")

        return review.to_dict(), 200


    @ns.expect(review_input, validate=True)
    @ns.marshal_with(review_output, code=200)
    def put(self, review_id):
        """Update review"""
        review = facade.update_review(review_id, ns.payload or {})

        if not review:
            ns.abort(404, "Review not found")

        return review.to_dict(), 200


    def delete(self, review_id):
        """Delete review"""
        ok = facade.delete_review(review_id)

        if not ok:
            ns.abort(404, "Review not found")

        return "", 204
