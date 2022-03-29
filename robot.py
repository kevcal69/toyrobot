from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Directions:
    NORTH = 'NORTH'
    SOUTH = 'SOUTH'
    WEST = 'WEST'
    EAST = 'EAST'


@dataclass
class Location(ABC):
    """ Location data that describes a position """

    @abstractmethod
    def where(self):
        """ Abstract method to describe current location for the object """


@dataclass
class Object(ABC):
    """ An object with location """
    id: str
    location: Optional[Location]


@dataclass
class DirectionXYCoordinate(Location):
    """ A subclass of location where it describes the x and y coordinate and direction """
    pos_x: int
    pos_y: int
    direction: str

    def where(self):
        return f'{self.pos_x},{self.pos_y} {self.direction}'


@dataclass
class ToyRobot(Object):
    """Toy robot that behaves in DirectionXYCoordinate """
    location: Optional[DirectionXYCoordinate]

