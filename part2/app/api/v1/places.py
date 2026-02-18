from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("places", description="Place operations")


# =========================
# Input model
# =========================

place_input = ns.model("PlaceInput", {
    "title": fields.String(required=True, description="Place title"),
    "description": fields.String(required=False, description="Description"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenities": fields.List(fields.String, description="Amenity IDs"),
})


# =========================
# Output model
# =========================

place_output = ns.model("PlaceOutput", {
    "id": fields.String,
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String,
})


# =========================
# Routes
# =========================

@ns.route("/")
class PlacesCollection(Resource):

    @ns.expect(place_input, validate=True)
    @ns.marshal_with(place_output, code=201)
    def post(self):
        place = facade.create_place(ns.payload or {})
        return place.to_dict(), 201


    @ns.marshal_list_with(place_output, code=200)
    def get(self):
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200



@ns.route("/<string:place_id>")
class PlaceItem(Resource):

    @ns.marshal_with(place_output, code=200)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, "Place not found")
        return place.to_dict(), 200


    @ns.expect(place_input, validate=True)
    @ns.marshal_with(place_output, code=200)
    def put(self, place_id):
        place = facade.update_place(place_id, ns.payload or {})
        if not place:
            ns.abort(404, "Place not found")
        return place.to_dict(), 200


    def delete(self, place_id):
        ok = facade.delete_place(place_id)
        if not ok:
            ns.abort(404, "Place not found")
        return "", 204
