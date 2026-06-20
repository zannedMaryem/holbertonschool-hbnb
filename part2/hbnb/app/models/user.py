from hbnb.app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        
        self.places = []
        self.reviews = []

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name):
        if not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("First name must be a string and less than 50 chararchters")
        self._first_name = first_name
    
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name):
        if not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("Last name must be a string and less than 50 chararchters")
        self._last_name = last_name
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        try:
            valid = validate_email(email, allow_smtputf8= True, check_deliverability=True)
            self._email = valid.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {str(e)}")
    
    @property
    def admin(self):
        return self._is_admin
    
    @admin.setter
    def admin(self, is_admin):
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean value (True or False)")
        self._is_admin = is_admin

    def add_place(self, place):
        from hbnb.app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instnace")
        self.places.append(place)
        place.owner = self

    def add_review(self, review):
        from hbnb.app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be a valid Review instance")
        self.reviews.append(review)
        review.user = self
