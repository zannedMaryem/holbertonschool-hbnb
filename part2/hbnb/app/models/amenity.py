from hbnb.app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.places = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError("The name of the amenity must be under 50 charachters")
        self._name = name


    def add_place(self, place):
        """Add places to amenity"""
        from hbnb.app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")
        if place not in self.places:
            self.places.append(place)
        if self not in place.amenities:       # avoid infinite loop
            place.amenities.append(self)
