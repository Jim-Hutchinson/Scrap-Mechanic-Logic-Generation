import numpy as np
import json

bodies = []
childs = []
indexes = []

def is_set(x, n):
  return x & 1 << n != 0

def add_gate(x, y, z, mode, color, id):
    indexes.append(id)
    childs.append(
        {
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
    )

def add_connection(fromID, toID):
    index = indexes.index(fromID)
    childs[index]["controller"]["controllers"].append(
        {"id": toID}
    )

def array_connect(fromArray, toArray):
    for fromID in fromArray:
        for toID in toArray:
            index = indexes.index(fromID)
            childs[index]["controller"]["controllers"].append(
                {"id": toID}
            ) 

size = int(input("Number of values: "))
width = int(input("Width of values: "))


# create self-wired XOR gates
for i in range(size*width):
    add_gate(i%width, np.floor(i/width), 3, 2, '111111', 900000+i)
    add_connection(900000+i, 900000+i)

# create comparison XOR gates
for i in range(size*width):
    add_gate(i%width, np.floor(i/width), 1, 2, '817C00', 800000+i)
    add_connection(900000+i, 800000+i)

# create output AND gates
outputAnds = [[0 for j in range(size)] for i in range(width)]
for i in range(size*width):
    add_gate(i%width, np.floor(i/width), 2, 0, '2CE6E6', 700000+i)
    outputAnds[i%width][int(np.floor(i/width))] = 700000+i
    add_connection(900000+i, 700000+i)

# create input AND gates
inputAnds = [[0 for j in range(size)] for i in range(width)]
for i in range(size*width):
    add_gate(i%width, np.floor(i/width), 0, 0, '0E8031', 600000+i)
    inputAnds[i%width][int(np.floor(i/width))] = 600000+i
    add_connection(600000+i, 900000+i)
    add_connection(800000+i, 600000+i)

# create output OR gates
for i in range(width):
    add_gate(i, -1, 0, 1, '0A3EE2', 500000+i)
for i in range(size):
    for j in range(width):
        add_connection(700000+i*width+j, 500000+j)

# create clock pulse gate
add_gate(width, size, 0, 1, 'E2DB13', 69)
for i in range(size*width):
    add_connection(69, 600000+i)

# create input OR gates
for i in range(width):
    add_gate(i, size, 0, 1, 'F5F071', 400000+i)
for i in range(size):
    for j in range(width):
        add_connection(400000+j, 800000+i*width+j)

# create decoder gates
decoderBits = int(np.floor(np.log2(size-1)+1))
for i in range(decoderBits):
    color = '7514ED'
    if i == 0:
        color = 'AE79F0'
    add_gate(width, size-1-i, 0, 1, color, 1000+i) # decoder input
    add_gate(width, size-1-i, 1, 0, '19E753', 2000+i) # decoder AND
    add_gate(width, size-1-i, 2, 4, '19E753', 3000+i) # decoder NOR
    add_connection(1000+i, 2000+i)
    add_connection(1000+i, 3000+i)
    
    # connect decoder to in/out AND gates
    andReceivers = []
    norReceivers = []
    for x in range(len(outputAnds)):
        for y in range(len(outputAnds[x])):
            if is_set(y, i):
                norReceivers.append(inputAnds[x][y])
                norReceivers.append(outputAnds[x][y])
            else:
                andReceivers.append(inputAnds[x][y])
                andReceivers.append(outputAnds[x][y])

    array_connect([2000+i], andReceivers)
    array_connect([3000+i], norReceivers)


dictionary = {
    'bodies': [
        {'childs': childs}
    ]
}

with open("C:\\Users\\kaiha\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561198799146619\\Blueprints\\6931a67c-c3bc-43f8-86ea-ffb8c6ae0fc9\\blueprint.json", "w") as outfile: 
    json.dump(dictionary, outfile)

