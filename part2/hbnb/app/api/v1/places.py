from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade
from hbnb.app.api.v1.users import user_model
from hbnb.app.api.v1.amenities import amenity_model

api = Namespace('places', description='Place operations')

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})
# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        if not place_data:
            return{'error': 'Invalid input data'}, 400
        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return{'error': str(e)}, 400
        return {
            'id': new_place.id,
            'title': new_place.title,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner': {
                'id': new_place.owner.id,
                'first_name': new_place.owner.first_name,
                'last_name': new_place.owner.last_name,
                'email': new_place.owner.email
            },
            'description': new_place.description
        }, 201

    @api.response(200, 'Places list retreived successfully')
    def get(self):
        """Retrive all places"""
        places_list = facade.get_all_places()
        return [
            {
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude,   
            } for place in places_list
        ], 200
  
@api.route('/<place_id>')
class PlaceResources(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return{'error':'Place not found'}, 404
        amenities_list = facade.get_amenities_by_place(place_id)
        return {
            'id': place.id,
            'title': place.title,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'description': place.description,
            'amenities': [
                {
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in amenities_list
            ]
        }, 200
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        if not place_data:
            return{'error': 'Invalid input data'}, 400
        try:
            place = facade.update_place(place_id, place_data)
        except ValueError as e:
            return{'error': str(e)}, 400
        if not place:
            return {'error':'Place not found'}, 404
        
        return {
            'title': place.title,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'description': place.description
        }, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return{'error': 'Place not found'}, 404
        reviews_list = facade.get_reviews_by_place(place_id)
        return[
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews_list
        ], 200

@api.route('/<place_id>/amenities')
class PlaceAmenitiesList(Resource):
    @api.response(200, 'List of amenities for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        "Get all amenities for a specific place"
        place = facade.get_place(place_id)
        if not place:
            return{'error': 'Place not found'}, 404
        amenities_list = facade.get_amenities_by_place(place_id)
        return[
            {
                'name': amenity.name
            } for amenity in amenities_list
        ], 200
