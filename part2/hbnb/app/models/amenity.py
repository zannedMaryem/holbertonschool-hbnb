from hbnb.app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError("The name of the amenity must be under 50 charachters")
        self._name = name
    