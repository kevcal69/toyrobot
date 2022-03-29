from abc import abstractmethod
from enum import Enum
from typing import Union

from action import Action
from robot import ToyRobot, Object, Location, Directions, DirectionXYCoordinate
from table import Plane


class SquareTableMove(Action):

    def __init__(self, obj: ToyRobot, plane: Plane):
        self.obj = obj
        self.plane = plane

    @abstractmethod
    def do(self) -> Union[Location, None]:
        pass


class LeftMove(SquareTableMove):

    def do(self) -> Union[Location, None]:
        """
            Rotate the object to -90 degrees from the object perspective
        """
        new_direction = None
        if self.obj.location.direction == Directions.NORTH:
            new_direction = Directions.WEST

        if self.obj.location.direction == Directions.SOUTH:
            new_direction = Directions.EAST

        if self.obj.location.direction == Directions.WEST:
            new_direction = Directions.SOUTH

        if self.obj.location.direction == Directions.EAST:
            new_direction = Directions.NORTH

        new_loc = DirectionXYCoordinate(
            pos_x=self.obj.location.pos_x, pos_y=self.obj.location.pos_y,
            direction=new_direction)
        obj = self.plane.place(self.obj, location=new_loc)
        if not obj:
            return
        return new_loc


class RightMove(SquareTableMove):

    def do(self) -> Union[Location, None]:
        """
            Rotate the object to +90 degrees from the object perspective
        """
        new_direction = None
        if self.obj.location.direction == Directions.NORTH:
            new_direction = Directions.EAST

        if self.obj.location.direction == Directions.SOUTH:
            new_direction = Directions.WEST

        if self.obj.location.direction == Directions.WEST:
            new_direction = Directions.NORTH

        if self.obj.location.direction == Directions.EAST:
            new_direction = Directions.SOUTH

        new_loc = DirectionXYCoordinate(
                pos_x=self.obj.location.pos_x, pos_y=self.obj.location.pos_y,
                direction=new_direction)
        obj = self.plane.place(self.obj, location=new_loc)
        if not obj:
            return
        return new_loc


class NormalMove(SquareTableMove):

    def do(self) -> Union[Location, None]:
        """ Do some table move action """
        new_loc = DirectionXYCoordinate(
            pos_y=self.obj.location.pos_y,
            pos_x=self.obj.location.pos_x,
            direction=self.obj.location.direction)
        if self.obj.location.direction == Directions.NORTH:
            new_loc.pos_y = self.obj.location.pos_y + 1
        if self.obj.location.direction == Directions.SOUTH:
            new_loc.pos_y = self.obj.location.pos_y - 1
        if self.obj.location.direction == Directions.WEST:
            new_loc.pos_x = self.obj.location.pos_x - 1
        if self.obj.location.direction == Directions.EAST:
            new_loc.pos_x = self.obj.location.pos_x + 1
        obj = self.plane.place(self.obj, location=new_loc)
        if not obj:
            return
        return new_loc


class PlaceMove(SquareTableMove):

    def __init__(self, obj: ToyRobot, plane: Plane, location: Location):
        super().__init__(obj, plane)
        self.location = location

    def do(self) -> Union[Location, None]:
        res = self.plane.place(self.obj, self.location)
        if res:
            return self.location
        return None


class Report(Action):

    def __init__(self, obj: ToyRobot):
        self.obj = obj

    def do(self) -> Union[str, None]:
        if self.obj is None or self.obj.location is None:
            return None
        return f'{self.obj.location.where()}'

