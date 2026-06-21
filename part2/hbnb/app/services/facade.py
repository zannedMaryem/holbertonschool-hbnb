from hbnb.app.persistence.repository import InMemoryRepository
from hbnb.app.models.user import User
from hbnb.app.models.place import Place
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
# User CRUD
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        return self.user_repo.update(user_id, user_data)
# Place CRUD
    """def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place"""
    def create_place(self, place_data):
    # Extract the owner data from the payload
        owner_data = place_data.pop('owner')

    # Fetch the existing user from the repository using their ID
        owner_id = owner_data.get('id')
        owner = self.user_repo.get(owner_id)

    # Validate that the owner exists
        if not owner:
            raise ValueError(f"User with ID {owner_id} not found")

    # Create the Place instance with the resolved User object
        place = Place(owner=owner, **place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        owner_data = place_data.pop('owner')
        owner_id = owner_data.get('id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"User with ID {owner_id} not found")
        place_data['owner'] = owner
        place = self.get_place(place_id)
        if not place:
            return None
        return self.place_repo.update(place_id, place_data)

# Amenity CRUD
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
    def get_amenities_by_place(self, place_id):
        return self.amenity_repo.get_by_attribute('place', self.place_repo.get(place_id))

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        return self.amenity_repo.update(amenity_id, amenity_data)

# Review CRUD
    def create_review(self, review_data):
    # Extract IDs from payload
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')

    # Fetch User and Place instances from repos
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")

    # Rating validation is already handled in Review class
        rating = review_data.get('rating')

    # Create Review with proper instances
        review = Review(
            text=review_data.get('text'),
            rating=rating,
            place=place,
            user=user
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute('place', self.place_repo.get(place_id))

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
