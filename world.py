import re
from uuid import uuid4
from abc import ABC, abstractmethod, abstractclassmethod
from typing import Optional, List, Any, Union

from action import Action
from action.ToyRobotActions import PlaceMove, NormalMove, LeftMove, RightMove, Report
from robot import ToyRobot, DirectionXYCoordinate
from table import SquareTable, Plane


class ToyRobotActionsEnum:
    PLACE = 'PLACE'
    MOVE = 'MOVE'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    REPORT = 'REPORT'


class InstructionParser(ABC):

    def __init__(self, instructions: list):
        self.instructions = instructions

    @abstractmethod
    def construct(self) -> List[Any]:
        """Construct the instructions into equivalent actions"""


class ActionFactory(ABC):
    ACTION: Optional[Action] = None

    def __init__(self, instruction: str, plane: SquareTable, obj: Optional[ToyRobot] = None):
        self.instruction = instruction
        self.obj = obj
        self.plane = plane

    def build(self):
        """ Call build """
        if self.ACTION is not None:
            action = self.ACTION(self.obj, self.plane)
            return action.do()

    @classmethod
    @abstractmethod
    def is_valid(cls, instruction: str) -> bool:
        pass


class PlaceMoveFactory(ActionFactory):
    ACTION = PlaceMove
    PATTERN = r'^(PLACE )([0-9]+),([0-9]+),(NORTH|SOUTH|WEST|EAST)$'

    def build(self):
        _, val = self.instruction.split(' ')
        matches = re.findall(self.PATTERN, self.instruction)

        _, x, y, direction = matches[0]
        try:
            loc = DirectionXYCoordinate(
                pos_x=int(x), pos_y=int(y), direction=direction)
        except Exception as e:
            print(e)
            return None
        action = self.ACTION(self.obj, self.plane, location=loc)
        return action.do()

    @classmethod
    def is_valid(cls, instruction) -> bool:
        return bool(re.match(cls.PATTERN, instruction))


class NormalMoveFactory(ActionFactory):
    ACTION = NormalMove

    @classmethod
    def is_valid(cls, instruction) -> bool:
        return instruction == ToyRobotActionsEnum.MOVE


class LeftMoveFactory(ActionFactory):
    ACTION = LeftMove

    @classmethod
    def is_valid(cls, instruction) -> bool:
        return instruction == ToyRobotActionsEnum.LEFT


class RightMoveFactory(ActionFactory):
    ACTION = RightMove

    @classmethod
    def is_valid(cls, instruction) -> bool:
        return instruction == ToyRobotActionsEnum.RIGHT


class ReportFactory(ActionFactory):
    ACTION = Report

    @classmethod
    def is_valid(cls, instruction) -> bool:
        return instruction == ToyRobotActionsEnum.REPORT

    def build(self):
        action = self.ACTION(self.obj)
        res = action.do()
        if res:
            print(res)
        return res


def process(instruction) -> Union[tuple, None]:
    if PlaceMoveFactory.is_valid(instruction):
        return instruction, ToyRobotActionsEnum.PLACE, PlaceMoveFactory
    if NormalMoveFactory.is_valid(instruction):
        return instruction, ToyRobotActionsEnum.MOVE, NormalMoveFactory
    if LeftMoveFactory.is_valid(instruction):
        return instruction, ToyRobotActionsEnum.LEFT, LeftMoveFactory
    if RightMoveFactory.is_valid(instruction):
        return instruction, ToyRobotActionsEnum.RIGHT, RightMoveFactory
    if ReportFactory.is_valid(instruction):
        return instruction, ToyRobotActionsEnum.REPORT, ReportFactory
    return None


class ToyRobotInstructionParser(InstructionParser):

    def construct(self):
        output = []
        for instruction in self.instructions:
            res = process(instruction)
            if res:
                output.append(res)
        return output


class WorldBuilder:

    def __init__(self, plane: Plane):
        self.plane = plane
        self.obj = None

    def process(self, instructions: list):
        start = False
        for instruction, type, factory in instructions:

            if not start and type == ToyRobotActionsEnum.PLACE:
                start = True
            if not start:
                continue

            # if type is place
            if type == ToyRobotActionsEnum.PLACE and not self.obj:
                self.obj = ToyRobot(id=str(uuid4()), location=None)

            factory_move = factory(instruction, self.plane, self.obj)
            location = factory_move.build()
            if isinstance(location, DirectionXYCoordinate):
                self.obj.location = location

            # restart the start value since this will most likely happen if initial
            # place command is invalid
            if self.obj.location is None:
                start = False
