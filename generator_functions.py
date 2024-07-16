import csv

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
    for i in range(int(len(array)*valWidth/targetWidth)):
        num = 0
        for j in range(int(targetWidth/valWidth)):
            shifted = (array[int((targetWidth/valWidth)*i+j)] << valWidth*j)
            num += shifted
        concat_array.append(num)
    return concat_array