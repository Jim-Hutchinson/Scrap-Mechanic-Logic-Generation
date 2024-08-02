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

# create master clock pulse gate
add_gate(width, size, 0, 1, 'E2DB13', 69)

#create and connect row gates
tickGates = int(((size*width)/255)+1)
count = 0
for i in range(tickGates):
    add_gate(width-i, size, 2, 1, 'E2DB13', 70+i)
    add_connection(69, 70+i)
    for j in range(255):
            if count == size*width:
                break
            else:
                add_connection(70+i,600000+count)
                count+=1

# create input OR gates
for i in range(width):
    add_gate(i, size, 0, 1, 'F5F071', 400000+i)
for i in range(size):
    for j in range(width):
        add_connection(400000+j, 800000+i*width+j)

#create decoder reciever gates
for i in range(size):
    add_gate(width,size-(i+1),2,0,'7514ED',100000+i)
    add_gate(width,size-(i+1),3,0,'CF11D2',300000+i)

# create input decoder gates
decoderBits = int(np.floor(np.log2(size-1)+1))
for i in range(decoderBits):
    color = '7514ED'
    if i == 0:
        color = 'AE79F0'
    add_gate(width+1, size-1-i, 0, 1, color, 1000+i) # decoder input
    add_gate(width, size-1-i, 0, 0, color, 2000+i) # decoder AND
    add_gate(width, size-1-i, 1, 4, color, 3000+i) # decoder NOR
    add_connection(1000+i, 2000+i)
    add_connection(1000+i, 3000+i)
    
    # connect decoder to in/out AND gates
    andReceivers = []
    norReceivers = []
    for x in range(size):
        if is_set(x, i):
            andReceivers.append(100000+x)
        else:
            norReceivers.append(100000+x)

    array_connect([2000+i], andReceivers)
    array_connect([3000+i], norReceivers)

# create output decoder gates
decoderBits = int(np.floor(np.log2(size-1)+1))
for i in range(decoderBits):
    color = 'CF11D2'
    if i == 0:
        color = 'EE7BF0'
    add_gate(width+1, decoderBits-1-i, 0, 1, color, 4000+i) # decoder input
    add_gate(width, decoderBits-1-i, 0, 0, color, 5000+i) # decoder AND
    add_gate(width, decoderBits-1-i, 1, 4, color, 6000+i) # decoder NOR
    add_connection(4000+i, 5000+i)
    add_connection(4000+i, 6000+i)
    
    # connect decoder to in/out AND gates
    andReceivers = []
    norReceivers = []
    for x in range(size):
        if is_set(x, i):
            andReceivers.append(300000+x)
        else:
            norReceivers.append(300000+x)

    array_connect([5000+i], andReceivers)
    array_connect([6000+i], norReceivers)



for y in range(size):
    inputLayer = []
    outputLayer = []
    for x in range(width):
        inputLayer.append(inputAnds[x][size-y-1])
        outputLayer.append(outputAnds[x][size-y-1])
    array_connect([100000+y], inputLayer)
    array_connect([300000+y], outputLayer)
    
    
dictionary = {
    'bodies': [
        {'childs': childs}
    ]
}

with open("C:\\Users\\jhutc\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561199013390109\\Blueprints\\ba486fdd-0b6f-4e45-ac78-fab28eaafa35\\blueprint.json", "w") as outfile: 
    json.dump(dictionary, outfile)
