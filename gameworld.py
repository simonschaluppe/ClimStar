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


# --- Game Flow / Actions --- #
class Action:
    def __init__(self, name, cost=0):
        self.name = name
        self.cost = cost
        self.effect = None


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


class DistrictType:
    NONE = "_"
    AGRICULTURE = "a"
    LOWRISE = "l"
    MIDRISE = "m"
    HIGHRISE = "H"
    INDUSTRY = "I"
    PUBLIC = "P"


def district_type_names() -> dict[str:str]:
    return {v: k for k, v in DistrictType.__dict__.items() if "_" not in k}


class District:
    buildings: list[Building]
    blocktype: DistrictType

    def __init__(self, id, position, blocktype=DistrictType.NONE):
        self.id = id
        self.position = position
        self.blocktype = blocktype
        self.support = 0

    def get_demand(self, service: ServiceType):
        demand = 0
        for building in self.buildings:
            demand += building.get_demand(service)
        return demand

    def increment_support(self, value):
        self.support += value

    def available_actions(self) -> list[Action]:
        a = Action("Gain local support", 1)
        a.execute = lambda: self.increment_support(1)
        return [a]

    def get_type_name(self) -> str:
        return district_type_names()[self.blocktype]

    def __repr__(self):
        return f"{self.id} - {self.get_type_name()}"


class City:
    districts: dict[tuple[int, int] : District]
    name: str

    def __init__(self):
        self.districts = {}
        self.center = (0, 0)

    def co2_emissions(self):
        return 301.2

    def get_ui(self):
        return f"""{self.name}
    
    Emissions: {self.co2_emissions()}"""

    def list_districts(self):
        return [d for d in self.districts.values()]

    def bounds(self):
        xmin = xmax = self.center[0]
        ymin = ymax = self.center[1]
        for pos in self.districts.keys():
            xmin = min(xmin, pos[0])
            xmax = max(xmax, pos[0])
            ymin = min(ymin, pos[1])
            ymax = max(ymax, pos[1])
        return xmin, xmax, ymin, ymax

    def get_grid(self):
        xmin, xmax, ymin, ymax = self.bounds()
        return [[(x, y) for y in range(ymin, ymax)] for x in range(xmin, xmax)]

    def get_tilemap(self) -> dict:
        return self.districts

    def __str__(self):
        xmin, xmax, ymin, ymax = self.bounds()
        s = ""
        for y in range(ymax, ymin - 1, -1):
            for x in range(xmin, xmax + 1):
                pos = (x, y)
                if pos not in self.districts:
                    s += " _ "
                else:
                    s += f" {self.districts[pos].blocktype} "
            s += "\n"

        return s


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
            block = District(
                id=i,
                position=position,
                blocktype=random.choice(list(district_type_names().keys())),
            )
            self.city.districts[position] = block


if __name__ == "__main__":
    g = Game()
    g.create_city()
    print(g.city.districts)
    print(g.city)
