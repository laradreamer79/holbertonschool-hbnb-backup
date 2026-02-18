from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("amenities", description="Amenity operations")

amenity_input = ns.model("AmenityInput", {
    "name": fields.String(required=True, description="Amenity name")
})

@ns.route("/")
class AmenityList(Resource):
    def get(self):
        amenities = facade.get_all_amenities()
        return [{"id": a.id, "name": a.name} for a in amenities], 200

    @ns.expect(amenity_input)
    def post(self):
        amenity = facade.create_amenity(ns.payload or {})
        return amenity.to_dict(), 201


@ns.route("/<string:amenity_id>")
class AmenityResource(Resource):
    def get(self, amenity_id):
        a = facade.get_amenity(amenity_id)
        if not a:
            ns.abort(404, "Amenity not found")
        return a.to_dict(), 200

    @ns.expect(amenity_input)
    def put(self, amenity_id):
        a = facade.update_amenity(amenity_id, ns.payload or {})
        if not a:
            ns.abort(404, "Amenity not found")
        return a.to_dict(), 200

    def delete(self, amenity_id):
        ok = facade.delete_amenity(amenity_id)
        if not ok:
            ns.abort(404, "Amenity not found")
        return "", 204
