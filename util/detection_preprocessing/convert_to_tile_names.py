import os
import sys

def main():
  input_file = sys.argv[1]
  output = sys.argv[2]
  with open(input_file) as f:
    lines = f.readlines()
  with open(output, 'w') as out:
    for line in lines:
      split = line.split('_',1)
      print(split)
      tile = split[1].replace('_nd','').replace('_des','').replace('jpeg','tif')
      out.write(tile)

if __name__ == '__main__':
  main()
