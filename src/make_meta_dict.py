import json
import tqdm
import sys
import ast

input_file = './meta_all.jsonl'
write_out = './meta_dict.json'

total_dict = {}
n = 180349

print('Processing input file...', flush = True)

with open(input_file, 'r+') as f:
    for index in tqdm.tqdm(range(n)):
        line = f.readline();
        if not line:
            break
        paper_dict = json.loads(line)
        paper_id = paper_dict['paper_id']
        total_dict[paper_id] = paper_dict

print('Dictionary created. Writing into output...', flush = True)
with open(write_out, 'w+') as f:
    json.dump(total_dict, f)
