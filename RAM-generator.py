import numpy as np
from generator_functions import *
from blueprint import *



bp = Blueprint()

size = int(input("Number of values: "))
width = int(input("Width of values: "))


# create self-wired XOR gates
for i in range(size*width):
    bp.add_gate(i%width, np.floor(i/width), 3, Mode.XOR, Color.BLACK, 900000+i)
    bp.connect(900000+i, 900000+i)

# create comparison XOR gates
for i in range(size*width):
    bp.add_gate(i%width, np.floor(i/width), 1, Mode.XOR, Color.DARK_YELLOW, 800000+i)
    bp.connect(900000+i, 800000+i)

# create output AND gates
outputAnds = [[0 for j in range(size)] for i in range(width)]
for i in range(size*width):
    bp.add_gate(i%width, np.floor(i/width), 2, Mode.AND, Color.TURQUOISE, 700000+i)
    outputAnds[i%width][int(np.floor(i/width))] = 700000+i
    bp.connect(900000+i, 700000+i)

# create input AND gates
inputAnds = [[0 for j in range(size)] for i in range(width)]
for i in range(size*width):
    bp.add_gate(i%width, np.floor(i/width), 0, Mode.AND, Color.DARK_GREEN, 600000+i)
    inputAnds[i%width][int(np.floor(i/width))] = 600000+i
    bp.connect(600000+i, 900000+i)
    bp.connect(800000+i, 600000+i)

# create output OR gates
for i in range(width):
    bp.add_gate(i, -1, 0, Mode.OR, Color.BLUE, 500000+i)
    
for i in range(size):
    for j in range(width):
        bp.connect(700000+i*width+j, 500000+j)

# create master clock pulse gate
bp.add_gate(width, size, 0, 1, Color.YELLOW, 69)

#create and connect row gates
tickGates = int(((size*width)/255)+1)
count = 0
for i in range(tickGates):
    bp.add_gate(width-i, size, 2, Mode.OR, Color.YELLOW, 70+i)
    bp.connect(69, 70+i)
    for j in range(255):
            if count == size*width:
                break
            else:
                bp.connect(70+i,600000+count)
                count+=1

# create input OR gates
for i in range(width):
    bp.add_gate(i, size, 0, Mode.OR, Color.YELLOW, 400000+i)
for i in range(size):
    for j in range(width):
        bp.connect(400000+j, 800000+i*width+j)

#create decoder reciever gates
for i in range(size):
    bp.add_gate(width, size-(i+1) , 2, Mode.AND, Color.DARK_PURPLE, 100000+i)
    bp.add_gate(width, size-(i+1) , 3, Mode.AND, Color.PURPLE, 300000+i)

# create input decoder gates
decoderBits = int(np.floor(np.log2(size-1)+1))
for i in range(decoderBits):
    color = Color.PURPLE if i==0 else Color.DARK_PURPLE
    bp.add_gate(width+1, size-1-i, 0, Mode.OR,  color, 1000+i) # decoder input
    bp.add_gate(width,   size-1-i, 0, Mode.AND, color, 2000+i) # decoder AND
    bp.add_gate(width,   size-1-i, 1, Mode.NOR, color, 3000+i) # decoder NOR
    bp.connect(1000+i, 2000+i)
    bp.connect(1000+i, 3000+i)
    
    # connect decoder to in/out AND gates
    andReceivers = []
    norReceivers = []
    for x in range(size):
        if is_set(x, i):
            andReceivers.append(100000+x)
        else:
            norReceivers.append(100000+x)

    bp.array_connect([2000+i], andReceivers)
    bp.array_connect([3000+i], norReceivers)

# create output decoder gates
decoderBits = int(np.floor(np.log2(size-1)+1))
for i in range(decoderBits):
    color = Color.LIGHT_PURPLE if i==0 else Color.PURPLE
    bp.add_gate(width+1, decoderBits-1-i, 0, Mode.OR,  color, 4000+i) # decoder input
    bp.add_gate(width,   decoderBits-1-i, 0, Mode.AND, color, 5000+i) # decoder AND
    bp.add_gate(width,   decoderBits-1-i, 1, Mode.NOR, color, 6000+i) # decoder NOR
    bp.connect(4000+i, 5000+i)
    bp.connect(4000+i, 6000+i)
    
    # connect decoder to in/out AND gates
    andReceivers = []
    norReceivers = []
    for x in range(size):
        if is_set(x, i):
            andReceivers.append(300000+x)
        else:
            norReceivers.append(300000+x)

    bp.array_connect([5000+i], andReceivers)
    bp.array_connect([6000+i], norReceivers)

for y in range(size):
    inputLayer = []
    outputLayer = []
    for x in range(width):
        inputLayer.append(inputAnds[x][size-y-1])
        outputLayer.append(outputAnds[x][size-y-1])
    bp.array_connect([100000+y], inputLayer)
    bp.array_connect([300000+y], outputLayer)
    

bp.write("blueprints/ram.json")
