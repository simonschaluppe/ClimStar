import math
import random
import string


class Flag:
    SPECIFIC = 1


class ServiceType:
    ELECTRICITY = 1
    HEAT = 2
    COOL = 3
    MOBILITY = 4


class Demand:
    type: ServiceType


class Supply:
    type: ServiceType


class UsageType:
    RESIDENTIAL = 1
    COMMERCIAL = 2
    INDUSTRIAL = 3
    RETAIL = 4
    OTHER = 5

    electricity_demand: Demand
    heat_demand: Demand
    mobility_demand: Demand


class Usage:
    type: UsageType
    area: float

    @property
    def electricity_demand(self):
        return self.type.electricity_demand * self.area


class Building:
    vintage: int
    gross_floor_area: float
    storeys: int
    usages: list[Usage]

    def get_electricity_demand(self, flags=None):
        ed = 0
        for usage in self.usages:
            ed += usage.electricity_demand
        if Flag.SPECIFIC in flags:
            ed = ed / self.gross_floor_area
        return ed


class BlockType:
    NONE = "_"
    AGRICULTURE = "a"
    LOWRISE = "l"
    MIDRISE = "m"
    HIGHRISE = "H"
    INDUSTRY = "I"
    PUBLIC = "P"


def blocktype_names() -> dict[str:str]:
    return {v: k for k, v in BlockType.__dict__.items() if "_" not in k}


class Block:
    buildings: list[Building]
    blocktype: BlockType

    def __init__(self, id, position, blocktype=BlockType.NONE):
        self.id = id
        self.position = position
        self.blocktype = blocktype

    def get_demand(self, service: ServiceType):
        demand = 0
        for building in self.buildings:
            demand += building.get_demand(service)
        return demand

    def __repr__(self):
        return f"{self.id} - {blocktype_names()[self.blocktype]}"


class District:
    demands: list[Demand]
    supplies: list[Supply]
    buildings: list[Building]


class City:
    districts: list[District]
    blocks: dict[tuple[int, int] : Block]
    name: str

    def __init__(self):
        self.blocks = {}
        self.center = (0, 0)

    def bounds(self):
        xmin = xmax = self.center[0]
        ymin = ymax = self.center[1]
        for pos in self.blocks.keys():
            xmin = min(xmin, pos[0])
            xmax = max(xmax, pos[0])
            ymin = min(ymin, pos[1])
            ymax = max(ymax, pos[1])
        return xmin, xmax, ymin, ymax

    def get_grid(self):
        xmin, xmax, ymin, ymax = self.bounds()
        return [[(x, y) for y in range(ymin, ymax)] for x in range(xmin, xmax)]

    def __str__(self):
        xmin, xmax, ymin, ymax = self.bounds()
        s = ""
        for y in range(ymax, ymin - 1, -1):
            for x in range(xmin, xmax + 1):
                pos = (x, y)
                if pos not in self.blocks:
                    s += " _ "
                else:
                    s += f" {self.blocks[pos].blocktype} "
            s += "\n"

        return s


# --- Game Flow / Actions --- #
class Action:
    def __init__(self, name, cost, required_meeples):
        self.name = name
        self.cost = cost
        self.required_meeples = required_meeples

    def execute(self, player):
        player.resources["support"] += 1


class Game:
    city: City

    def __init__(self):
        pass

    def get_grid_positions(self, amount, pattern=None, start=(0, 0)):
        positions = [start]
        length = int(math.sqrt(amount) / 2)
        while len(positions) < amount:
            pos = (
                int(random.gauss(start[0], length)),
                int(random.gauss(start[1], length)),
            )
            if pos not in positions:
                positions.append(pos)
        return positions

    def create_city(self):
        self.city = City()
        self.city.name = "Aloni"
        for i, position in enumerate(
            self.get_grid_positions(10, start=self.city.center)
        ):
            block = Block(
                id=i,
                position=position,
                blocktype=random.choice(list(blocktype_names().keys())),
            )
            self.city.blocks[position] = block


if __name__ == "__main__":
    g = Game()
    g.create_city()
    print(g.city.blocks)
    print(g.city)
