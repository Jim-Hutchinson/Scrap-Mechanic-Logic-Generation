import numpy as np
from generator_functions import *
from blueprint import *



bp = Blueprint()



def make_decoder(outputs, outWidth):
    # places top row of AND gates
    for i in range(len(outputs)):
        bp.add_gate(-(i%8), i//8, 2, Mode.AND, Color.ORANGE, 5000+i)
        bp.connect(9000+i, 5000+i)

    # places top row of OR gates
    for i in range(outWidth):
        bp.add_gate(-i, 0, 3, Mode.OR, Color.BLUE if i==0 else Color.DARK_BLUE, 2000+i)
        bp.array_connect([5000+j*outWidth+i for j in range(len(outputs)//outWidth)], [2000+i])

    # places gates for decoder
    it = int(np.floor(np.log2(len(outputs)/outWidth - 1) + 1))
    for j in range(it):
        color = Color.LIGHT_GREEN if j==0 else Color.DARK_GREEN
        bp.add_gate(-j,  0, 0, Mode.NOR, color, 3000+j)
        bp.add_gate(-j, -1, 0, Mode.AND, color, 6000+j)
        bp.add_gate(-j, -2, 0, Mode.OR,  color, 7000+j)
        bp.add_gate(-j, -3, 0, Mode.OR,  color, 7500+j)
        bp.connect(7500+j, 7000+j)
        bp.connect(7000+j, 6000+j)
        bp.connect(7000+j, 3000+j)

        # connect decoder to top gates
        ands = []
        nors = []
        for k in range(int(len(outputs)/outWidth)):
            if is_set(k,j):
                for l in range(outWidth): ands.append(5000+outWidth*k+l)
            else:
                for l in range(outWidth): nors.append(5000+outWidth*k+l)

        bp.array_connect([6000+j], ands)
        bp.array_connect([3000+j], nors)



array = csv_array("data/test.csv")

outWidth = max(array, key=lambda n: abs(n)).bit_length()
outWidth += 1 if min(array) < 0 else 0
print("outwidth: ", outWidth)

bits = int(2**np.floor(np.log2(np.sqrt(len(array)-1))) * (outWidth/2))
bits *= 2 if len(array) <= 4 else 1
print("bits: ", bits)

decoderBits = int(np.floor(np.log2(bits/outWidth-1)+1))

array = twos_complement(array, outWidth)
array = bit_concat(array, outWidth, bits)

inputBitwidth = (len(array)-1).bit_length()


# create input gates
for i in range(inputBitwidth):
    bp.add_gate(-bp.count_gates()-decoderBits, -3, 0, Mode.OR, 
        Color.LIGHT_GREEN if i==0 else Color.DARK_GREEN, 
        bp.count_gates())

# create output gates
for i in range(bits):
    bp.add_gate(-(i%8), i//8, 1, Mode.XOR, 
        Color.RED if i==0 else Color.DARK_BROWN, 
        9000+(bp.count_gates()-inputBitwidth))

# add NOR gate
bp.add_gate(0, 1, 0, Mode.NOR, Color.BLACK, 8000)

norGate = 1

# connects from input
for i in range(inputBitwidth):
    if decimalToBinary(norGate, inputBitwidth)[i] == '1':
        bp.connect(inputBitwidth-1-i, 8000)

# connects to output
for i in range(bits):
    if decimalToBinary(array[0], bits)[i] == '1':
        bp.connect(8000, 9000+(bits-1-i))

prevFlips = [0] * len(array)
placeIndex = 1

#      This 1  v   excludes the first array item since it is handled by the NOR gate
for i in range(1, len(array)):
    currentFlips = 0                # keeps track of bits that need to flip as we go
    if i & norGate == 0:            # detects when the NOR gate is active
        currentFlips = array[0]     # if so, flip bits corresponding to NOR gate connections(first value)
    #      This 1  v   excludes address 0 since no other address will ever contain address 0 
    for j in range(1, i):
        if i & j == j:              # checks address i also contains address j within it
            currentFlips ^= prevFlips[j] # if so, incorperate that address's flips too

    currentFlips ^= array[i]
    prevFlips[i] = currentFlips

    outputFlips = decimalToBinary(currentFlips, bits)
    if outputFlips != '000':

        # create logic gate 
        bp.add_gate(-(placeIndex % 8), 1+(placeIndex//8 % 8), 
            -(bp.count_gates()-bits-inputBitwidth)//64, Mode.AND, Color.BLACK, 1000+i)
        
        # connect from input
        for j in range(inputBitwidth):
            if decimalToBinary(i, inputBitwidth)[j] == '1':
                bp.connect(inputBitwidth-1-j, 1000+i)

        # connect to output
        for j in range(bits):
            if outputFlips[j] == '1':
                bp.connect(1000+i, 9000+(bits-1-j))


make_decoder([9000+i for i in range(bits)], outWidth)


bp.write("blueprints/xor-rom.json")
