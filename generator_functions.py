import csv
import numpy as np



def csv_array(filename):
  flattened_list = []
  with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      for item in row:
        flattened_list.append(int(item))
  return flattened_list


def twos_complement(array, bits):
  conv_array = []
  mask = (1 << bits) - 1
  for n in array:
    conv_array.append(int(n&mask))
  return conv_array
        

def bit_concat(array, valWidth, targetWidth):
    concat_array = []
    for i in range(int(np.ceil(len(array)*valWidth/targetWidth))):
        num = 0
        for j in range(int(targetWidth/valWidth)):
            try:
              shifted = (array[int((targetWidth/valWidth)*i+j)] << valWidth*j)
              num += shifted
            except: pass
        concat_array.append(num)
    #print(concat_array)
    return concat_array


def is_set(x, n):
  return x & 1 << n != 0


def decimalToBinary(n, bits): 
    binary = bin(n).replace("0b", "")
    for i in range(bits-len(binary)):
        binary = "0" + binary
    return binary
