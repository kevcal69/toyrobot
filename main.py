from abc import ABC, abstractmethod
from typing import List

from table import SquareTable
from world import ToyRobotInstructionParser, WorldBuilder


class IOHandler(ABC):

    @abstractmethod
    def read(self) -> List[str]:
        """ Do reads """


class FileInput(IOHandler):

    def __init__(self, filename):
        self.filename = filename

    def read(self) -> List[str]:
        with open(self.filename) as fp:
            lines = fp.readlines()
            return [
                line.strip()
                for line in lines
            ]



if __name__ == '__main__':
    handler = FileInput('instructions.txt')
    instructions_str = handler.read()
    parser = ToyRobotInstructionParser(instructions=instructions_str)
    instruction = parser.construct()

    square_table = SquareTable(dimension=5)
    world = WorldBuilder(plane=square_table)
    world.process(instruction)



