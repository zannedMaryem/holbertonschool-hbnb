
from hbnb.app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError

import re


class User(BaseModel):
    """Class that describes the user model and sets attribute requirments"""
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        
        self.places = []
        self.reviews = []

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name):
        if not isinstance(first_name, str):
            raise ValueError("First name must be a string")
        if len(first_name) > 50:
            raise ValueError("First name must be less than 50 characters")
        if not first_name.strip():
            raise ValueError("First name cannot be empty")
        self._first_name = first_name
    
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name):
        if not isinstance(last_name, str):
            raise ValueError("Last name must be a string")
        if len(last_name) > 50:
            raise ValueError("Last name must be less than 50 characters")
        if not last_name.strip():
            raise ValueError("Last name cannot be empty")
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
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self.hash_password(password)

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
        # Only append the place once
        if place not in self.places:
            self.places.append(place)
        # Ensure the place owns this user as its owner, but avoid infinite recursion
        if place.owner is not self:
            place.owner = self

    def add_review(self, review):
        from hbnb.app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be a valid Review instance")
        if review not in self.reviews:
            self.reviews.append(review)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from hbnb.app import bcrypt   
        self._validate_password(password)
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')    
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from hbnb.app import bcrypt
        return bcrypt.check_password_hash(self.password, password)

    def _validate_password(self, password):
        """Validates password requirments"""
        if not isinstance(password, str):
            raise ValueError("password must be a string")
        if len(password) > 72:
            raise ValueError("password too long and must be under 72 characters")
        if len(password) < 8:
            raise ValueError("password too short and must be over 8 characters")
        if not re.search(r"[A-Z]", password):
            raise ValueError("password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", password):
            raise ValueError("password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("password must contain at least one special character")
