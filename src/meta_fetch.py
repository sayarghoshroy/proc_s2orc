import sys
import ast
import requests
import json
import tqdm

read_file = 'file_to_be_read'
IDs_file = 'file_with_valid_IDs'
out_file = 'output_file'

MAX_PROC = int(1e10)

args = sys.argv
# 1: read_file, 2: IDs file, 3:output file, 4: file ID
read_file = args[1]
IDs_file = args[2]
out_file = args[3]
file_ID = args[4]

with open(IDs_file, 'r+') as f:
  IDs = set(json.load(f))

with open(read_file, 'r+') as f:
  for counter in range(MAX_PROC):
    line = f.readline()
    if not line:
        break
    meta_dict = json.loads(line)
    paper_ID = meta_dict['paper_id']

    if paper_ID in IDs:
      # Valid ID
      with open(out_file, 'a+') as o:
        o.write(str(json.dumps(ast.literal_eval(str(meta_dict)))))
        o.write('\n')

print()
print('Number of items:', counter)
