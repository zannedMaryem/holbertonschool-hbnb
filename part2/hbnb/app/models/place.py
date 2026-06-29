from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.user import User


class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description = None):
        super().__init__()
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.description = description
        self.reviews = []
        self.amenities = []
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        # title must be a string and under 100 charachters
        if not isinstance(title, str):
            raise ValueError("The title must be a string")
        if len(title) > 100:
            raise ValueError("The title must be under 100 charachters")
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self._title = title
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        # price must be a positive float
        if not isinstance(price, (float, int)) or price < 0:
            raise ValueError("The price per night must be a positive float")
        self._price = float(price)

    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self,latitude):
        # latitude must be a float and:  -90.0 < latitude < 90.0
        if not isinstance(latitude, (float, int)) or latitude < -90.0 or latitude > 90.0:
            raise ValueError("The latitude must be between -90.0 and 90.0")
        self._latitude = latitude
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, longitude):
        # longitude must be a float and: -180.0 < longitude < 180.0
        if not isinstance(longitude, (float, int)) or longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")
        self._longitude = longitude

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, owner):
        # owner must be a valid User instance
        if not isinstance(owner, User):
            raise ValueError("owner must be a valid User instance")
        # If this place already belongs to this owner, do nothing
        if getattr(self, '_owner', None) is owner:
            return
        self._owner = owner
        # Maintain the bidirectional reference without recursive setter calls
        if self not in owner.places:
            owner.places.append(self)
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        # description is optional and if it's available must be a string
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("Description must be a paragraph that describes your location")
        self._description = description

    def add_review(self, review):
        """Add a review to a place"""
        from hbnb.app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("review must be a valid Review instance")
        if review not in self.reviews:
            self.reviews.append(review)
    
    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from hbnb.app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be a valid Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
        if self not in amenity.places:         # avoid infinite loop
            amenity.places.append(self)
