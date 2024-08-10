import json
from enum import Enum, IntEnum



class Mode(IntEnum):
    AND     = 0
    OR      = 1
    XOR     = 2
    NAND    = 3
    NOR     = 4
    XNOR    = 5



class Color(str, Enum):
    RED             = 'FF0000'
    ORANGE          = 'DF7F01'
    YELLOW          = 'E2DB13'
    DARK_YELLOW     = '817C00'
    DARK_BROWN      = '560202'
    LIGHT_GREEN     = '19E753'
    DARK_GREEN      = '064023'
    TURQUOISE       = '2CE6E6'
    BLUE            = '0000FF'
    DARK_BLUE       = '00007F'
    LIGHT_PURPLE    = 'EE7BF0'
    PURPLE          = 'CF11D2'
    DARK_PURPLE     = '7514ED'
    BLACK           = '111111'
    GRAY            = '7F7F7F'
    WHITE           = 'FFFFFF'



class Blueprint:

    def __init__(self):
        self.childs = {}


    def add_gate(self, x, y, z, mode, color, id):
        self.childs[id] = {
            "color": color,
            "controller": {
                "active": False,
                "controllers": [],
                "id": id,
                "joints": None,
                "mode": mode
            },
            "pos": {
                "x": x,
                "y": y,
                "z": z
            },
            "shapeId": "9f0f56e8-2c31-4d83-996c-d00a9b296c3f",
            "xaxis": -2,
            "zaxis": -1
        }


    def connect(self, fromID, toID):
        self.childs[fromID]["controller"]["controllers"].append(
            { "id": toID }
        )


    def array_connect(self, fromArray, toArray):
        for fromID in fromArray:
            for toID in toArray:
                self.connect(fromID, toID)
        

    def count_gates(self):
        return len(self.childs)


    def write(self, file, indent=4):
        print("number of gates: ", self.count_gates())
        j = {
            "bodies": [
                { "childs": self.childs }
            ]
        }
        with open(file, 'w') as f:
            json.dump(j, f, indent=indent)
