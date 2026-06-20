from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.place import Place
from hbnb.app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not isinstance(text, str):
            raise ValueError("Add a text to your review")
        self.text = text
        if not isinstance(rating, int) or rating not in range(1,6):
            raise ValueError("Your rating must be between 1 and 5")
        self.rating = rating
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")
        self.place = place
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")
        self.user = user
        place.add_review(self)
        user.add_review(self)
        
