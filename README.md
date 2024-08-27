XOR-ROM:

Generates a logic lookup table of N-bit values as stored in a CSV file. Data is stored in the connections between gates.

Max storage size is in theory 1MB, but the game cannot spawn this from the lift
and gates are exceeding the connection limit.

  To use:
  Place the csv file in the same folder as the program files.
  Replace the blueprint file path with a blueprint of your own to overwrite.
  **This blueprint will be overwritten every time the program is run, so save your lookups elsewhere if you want to keep them."**
  Run the generation code with Python.
  Enter the name of the CSV file without ".csv"

RAM_Generator:

Generates a RAM bank with specified word width and word count.

  To use:
  Replace the blueprint file path with a blueprint of your own to overwrite.
  **This blueprint will be overwritten every time the program is run, so save your RAM builds elsewhere if you want to keep them."**
  Run the program with Python.
  Enter the parameters of the RAM you wish to create.
