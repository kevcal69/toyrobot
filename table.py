from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union

from robot import Object, Location, DirectionXYCoordinate


@dataclass
class Plane(ABC):
    """ A class that describes space where u can put Any object in it """

    objects: Optional[dict] = None

    def place(self, obj: Object, location: Location) -> Union[Object, None]:
        """ Add an object in the plane """

        if not self.can_place(location):
            # raise exception or return none
            return
        if not self.objects:
            self.objects = {}
        if obj.id not in self.objects:
            self.objects.update({
                obj.id: obj
            })
        return obj

    @abstractmethod
    def can_place(self, location) -> bool:
        pass


class SquareTable(Plane):
    """ Square table with 2 dimension (x,y) """

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension

    def can_place(self, location: DirectionXYCoordinate) -> bool:
        """ Check if location is over the boundary of x and y axis of square table"""
        if (location.pos_x < 0 or location.pos_x > self.dimension - 1) or\
                (location.pos_y < 0 or location.pos_y > self.dimension - 1):
            return False
        return True

