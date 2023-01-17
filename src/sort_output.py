import json
import sys
import ast
import tqdm

combined_out = './rel_work_all.jsonl'
sorted_out = './relw_final.jsonl'

total_out = []

print('Reading input file...', flush = True)

with open(combined_out, 'r+') as f:
  while True:
    line = f.readline();
    if not line:
        break
    paper_dict = json.loads(line)
    if len(paper_dict['possible_rel_works']) > 0:
        total_out.append(paper_dict)

total_out = sorted(total_out, key = lambda k : k['possible_rel_works'][0][1], reverse = True)
print('Items Sorted', flush = True)

for item in tqdm.tqdm(total_out):
  with open(sorted_out, 'a+') as o:
    o.write(str(json.dumps(ast.literal_eval(str(item)))))
    o.write('\n')

print('Done.', flush = True)

