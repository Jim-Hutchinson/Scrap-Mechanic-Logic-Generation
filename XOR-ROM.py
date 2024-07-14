import random
import numpy as np
import json

def decimalToBinary(n, bits): 
    binary = bin(n).replace("0b", "")
    for i in range(bits-len(binary)):
        binary = "0" + binary
    return binary



Noutputs = int(input("Number of values: "))
outWidth = int(input("Bit width of values: "))
hasDecoder = False
decode = input("Make Decoder? [Y/N]: ")
if(decode == 'Y'): hasDecoder = True

bitCount = Noutputs*outWidth
Width = int(2**np.floor(np.log2(np.sqrt(bitCount-1))+1))

bodies = []
childs = []
indexes = []
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

def is_set(x, n):
  return x & 1 << n != 0

def make_decoder(outputs, outWidth, inWidth):
    
    #places top row of AND gates
    for i in range(len(outputs)):
        add_gate(-i,0,2,0,'DF7F01',5000+i)
        add_connection(9000+i,5000+i)

    #places top row of OR gates
    for i in range(outWidth):
        color = '0F2E91'
        if i==0:
            color = '4C6FE3'
        add_gate(-i,0,3,1,color,2000+i)
        inAnds = [5000+j*outWidth+i for j in range(int(len(outputs)/outWidth))]
        array_connect(inAnds, [2000+i])

    
    #places gates for decoder
    for j in range(int(np.floor(np.log2(len(outputs)/outWidth-1)+1))):
        color = '0E8031'
        if j==0:
            color = '68FF88'
        add_gate(-j-inWidth,0,0,4, color,3000+j) # NOR gates
        add_gate(-j-inWidth,-1,0,0, color,6000+j) # AND gates
        add_gate(-j-inWidth,-2,0,1, color,7000+j) # input OR gates
        add_gate(-j-inWidth,-3,0,1, color,7500+j) # input OR gates
        add_connection(7500+j,7000+j)
        add_connection(7000+j,6000+j)
        add_connection(7000+j,3000+j)

        #connect decoder to top gates
        ands = []
        nors = []
        andIn = [6000+j]
        norIn = [3000+j]
        for k in range(int(len(outputs)/outWidth)):
            if is_set(k,j):
                for l in range(outWidth): ands.append(5000+outWidth*k+l)
            else:
                for l in range(outWidth): nors.append(5000+outWidth*k+l)

        array_connect(andIn, ands)
        array_connect(norIn, nors)

#norGate = int('100',2) # which switch is the NOR gate connected to(converts to int for easier calculations later)
norGate = 1

#array = [3, 4, 1, 3, 0, 6, 4, 0] # output we want from the ROM
array = [random.randint(0, (2**Width-1)) for _ in range(Width)]

bits = max(array).bit_length() # bitwidth of output
inputBitwidth = (len(array)-1).bit_length()

prevFlips = [0]*len(array)
gateCount = 0

# create input gates
for i in range(inputBitwidth):
    color = "064023"
    if i == 0:
        color = "19E753"
    add_gate(-gateCount, -3, 0, 1, color, gateCount)
    gateCount += 1

# create output gates
for i in range(bits):
    color = "560202"
    if i == 0:
        color = "D02525"
    add_gate(-gateCount+inputBitwidth, 0, 1, 2, color, 9000+(gateCount-inputBitwidth))
    gateCount += 1

# add NOR gate
add_gate(0, 1, 0, 4, "111111", 8000)

# connects from input
for i in range(inputBitwidth):
    if decimalToBinary(norGate, inputBitwidth)[i] == '1':
        add_connection(inputBitwidth-1-i, 8000)

# connects to output
for i in range(bits):
    if decimalToBinary(array[0], bits)[i] == '1':
        add_connection(8000, 9000+(bits-1-i))
gateCount += 1

#      This 1  v   excludes the first array item since it is handled by the NOR gate
for i in range(1, len(array)):
    currentFlips = 0 # keeps track of bits that need to flip as we go
    if i & norGate == 0: # detects when the NOR gate is active
        currentFlips = array[0] # if so, flip bits corresponding to NOR gate connections(first value)
    #      This 1  v   excludes address 0 since no other address will ever contain address 0 
    for j in range(1, i):
        if i & j == j: # checks address i also contains address j within it
            currentFlips ^= prevFlips[j] # if so, incorperate that address's flips too

    currentFlips ^= array[i]
    prevFlips[i] = currentFlips



    outputFlips = decimalToBinary(currentFlips, bits)
    if outputFlips != '000':
        print(outputFlips)
        # create logic gate
        add_gate(-((gateCount-bits-inputBitwidth) % max(bits, inputBitwidth)), 1+np.floor((gateCount-bits-inputBitwidth)/max(bits, inputBitwidth)), 0, 0, "111111", 1000+i)
        
        # connect from input
        for j in range(inputBitwidth):
            if decimalToBinary(i, inputBitwidth)[j] == '1':
                add_connection(inputBitwidth-1-j, 1000+i)

        # connect to output
        for j in range(bits):
            if outputFlips[j] == '1':
                add_connection(1000+i, 9000+(bits-1-j))
        gateCount += 1

if hasDecoder:
    make_decoder([9000+i for i in range(bits)],outWidth,inputBitwidth)


print(array)
print("Gate Count: " + str(gateCount))
dictionary = {
    'bodies': [
        {'childs': childs}
    ]
}

with open("C:\\Users\\jhutc\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User\\User_76561199013390109\\Blueprints\\ba486fdd-0b6f-4e45-ac78-fab28eaafa35\\blueprint.json", "w") as outfile: 
    json.dump(dictionary, outfile)