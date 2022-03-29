from uuid import uuid4

from robot import ToyRobot
from table import SquareTable
from world import ToyRobotInstructionParser, ToyRobotActionsEnum, PlaceMoveFactory, NormalMoveFactory, LeftMoveFactory, \
    ReportFactory, WorldBuilder

INSTRUCTIONS = [
    'PLACE 1,2,EAST',
    'MOVE',
    'MOVE',
    'LEFT',
    'REPORT'
]
PARSE_INSTRUCTION = [
    ('PLACE 1,2,EAST', ToyRobotActionsEnum.PLACE, PlaceMoveFactory),
    ('MOVE', ToyRobotActionsEnum.MOVE, NormalMoveFactory),
    ('MOVE', ToyRobotActionsEnum.MOVE, NormalMoveFactory),
    ('LEFT', ToyRobotActionsEnum.LEFT, LeftMoveFactory),
    ('REPORT', ToyRobotActionsEnum.REPORT, ReportFactory),
]


def test_parser():
    parser = ToyRobotInstructionParser(
        instructions=INSTRUCTIONS
    )
    parsed_instruction = parser.construct()
    assert all([all([a[0] == b[0], a[1] == b[1], a[2] == b[2]]) for a, b in zip(parsed_instruction, PARSE_INSTRUCTION)])


def test_robot_state():
    parser = ToyRobotInstructionParser(
        instructions=INSTRUCTIONS
    )
    parsed_instruction = parser.construct()

    square_table = SquareTable(dimension=5)
    robot = ToyRobot(id=str(uuid4()), location=None)

    # test state of the robot here
    # this is sequential test to test the current position of the robot
    # base on the set instruction above

    # 'PLACE 1,2,EAST'
    factory = PlaceMoveFactory('PLACE 1,2,EAST', square_table, robot)
    location = factory.build()
    robot.location = location

    assert robot.location.pos_x == 1
    assert robot.location.pos_y == 2
    assert robot.location.direction == 'EAST'

    # MOVE
    factory = NormalMoveFactory('MOVE', square_table, robot)
    location = factory.build()
    robot.location = location

    assert robot.location.pos_x == 2
    assert robot.location.pos_y == 2
    assert robot.location.direction == 'EAST'

    # MOVE
    factory = NormalMoveFactory('MOVE', square_table, robot)
    location = factory.build()
    robot.location = location

    assert robot.location.pos_x == 3
    assert robot.location.pos_y == 2
    assert robot.location.direction == 'EAST'

    # LEFT
    factory = LeftMoveFactory('LEFT', square_table, robot)
    location = factory.build()
    robot.location = location

    assert robot.location.pos_x == 3
    assert robot.location.pos_y == 2
    assert robot.location.direction == 'NORTH'

    # REPORT
    factory = ReportFactory('REPORT', square_table, robot)
    report = factory.build()

    assert report == robot.location.where()
    assert robot.location.pos_x == 3
    assert robot.location.pos_y == 2
    assert robot.location.direction == 'NORTH'

    ## SITUATIONAL TEST
    # for additional situations and checks for functionality

    # Place the robot to another place
    assert robot.location.pos_x == 3  # assert initial values
    assert robot.location.pos_y == 2  # assert initial values
    assert robot.location.direction == 'NORTH'  # assert initial values

    # do action
    factory = PlaceMoveFactory('PLACE 0,0,WEST', square_table, robot)
    location = factory.build()
    robot.location = location

    assert robot.location.pos_x == 0
    assert robot.location.pos_y == 0
    assert robot.location.direction == 'WEST'

    # Place the robot to impossible  place
    assert robot.location.pos_x == 0  # assert initial values
    assert robot.location.pos_y == 0  # assert initial values
    assert robot.location.direction == 'WEST'  # assert initial values

    # do action
    factory = PlaceMoveFactory('PLACE 6,5,WEST', square_table, robot)
    location = factory.build()

    assert location is None
    assert robot.location.pos_x == 0
    assert robot.location.pos_y == 0
    assert robot.location.direction == 'WEST'


    # MOVE the robot to impossible place
    assert robot.location.pos_x == 0  # assert initial values
    assert robot.location.pos_y == 0  # assert initial values
    assert robot.location.direction == 'WEST'  # assert initial values

    # do action
    factory = NormalMoveFactory('MOVE', square_table, robot)
    location = factory.build()

    assert location is None
    assert robot.location.pos_x == 0
    assert robot.location.pos_y == 0
    assert robot.location.direction == 'WEST'


def test_overall():
    """Test run for everything no assertion"""
    instruction_1 = [
        'PLACE 1,2,EAST',
        'MOVE',
        'MOVE',
        'RIGHT',
        'REPORT'
    ]
    parser = ToyRobotInstructionParser(instructions=instruction_1)
    instruction = parser.construct()

    square_table = SquareTable(dimension=5)
    world = WorldBuilder(plane=square_table)
    world.process(instruction)

    instruction_2 = [
        'PLACE 1,10,EAST',
        'PLACE 1,2,EAST',
        'MOVE',
        'MOVES',
        'LEFT',
        'REPORT'
    ]
    parser = ToyRobotInstructionParser(instructions=instruction_1)
    instruction = parser.construct()

    square_table = SquareTable(dimension=5)
    world = WorldBuilder(plane=square_table)
    world.process(instruction)
