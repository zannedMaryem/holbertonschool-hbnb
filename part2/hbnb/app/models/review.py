from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.place import Place
from hbnb.app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        place.add_review(self)
        user.add_review(self)
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        if not isinstance(text, str):
            raise ValueError("Review text must be a string")
        if not text.strip():
            raise ValueError("text cannot be empty")
        self._text = text
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, rating):
        if not isinstance(rating, int):
            raise ValueError("Your rating must be an integer")
        if rating not in range(1,6):
            raise ValueError("Your rating must be between 1 and 5")
        self._rating = rating
    
    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, place):
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")
        self._place = place
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")
        self._user = user
