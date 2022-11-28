import nltk
import numpy as np
import re
import sys
import ast
import requests
import json
import tqdm

# Uncomment to download required resources
# nltk.download('punkt')
# nltk.download('stopwords')

from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

read_file = 'file_to_be_read'
rel_work_file = 'output_file'

MAX_PROC = int(1e6)

def normalize(name):
  name = name.lower().strip()
  re.sub('\s+', ' ', name)
  return name

def check_rel_work(body_text):
  for blob in body_text:
    if normalize(blob['section']) == 'related work':
      return True, blob
  return False, None

def get_following_sections(body_text):
  flag = 0
  following_sections = []

  for blob in body_text:
    if flag == 0 and normalize(blob['section']) == 'related work':
      flag = 1
      continue
    if flag == 1:
      following_sections.append(blob['section'])

  return following_sections

def score_sections(section_id, count_sections, common_tokens, count_tokens):
  score = (count_sections - section_id) / count_sections + (common_tokens / count_tokens)
  return score

def penalty(section_name):
  searched = re.search('[a-zA-Z]', section_name)
  if searched is None:
    return True

  bad_names = ['conclusion', 'discussion', 'introduction', 'future work',
               'ablation', 'experiment', 'result', 'outcome', 'method',
               'formulation', 'problem', 'appendix', 'overview', 'category',
               'formalization', 'implementation', 'case studies', 'case study',
               'evaluation', 'approach', 'summary', 'demo', 'proof', 'preprocess',
               'limitation', 'statistics', 'user study', 'user studies', 'proposed',
               'baseline', 'objective', 'note', 'figure', 'dataset', 'observation']

  for name in bad_names:
    if name in section_name:
      return True
  return False

def get_rel_work(candidate_sections, blob):
  # if a subsequent section name has tokens contained in the related work section

  rel_works = []
  topics_set = set()
  tokens_blob = set(nltk.word_tokenize(blob['text'].lower()))
  num_sections = len(candidate_sections)

  for index, candidate in enumerate(candidate_sections):
    if candidate.lower().strip() == 'related work':
      continue

    if candidate.lower().strip() in topics_set:
      continue

    topics_set.add(candidate.lower().strip())
    candidate_tokens = nltk.word_tokenize(candidate.lower())
    common = tokens_blob.intersection(candidate_tokens)
    common = common.difference(stops)

    if not penalty(candidate.lower().strip()):
      score = score_sections(index + 1, num_sections, len(common), len(candidate_tokens))
    else:
      score = -1

    rel_works.append([candidate.lower().strip(),
                      score,
                      index + 1,
                      len(common)])
    # Format: text, score, index, overlap

  sorted_works = sorted(rel_works, key = lambda works: works[1], reverse = True)
  return sorted_works

args = sys.argv
# 1: read_file, 2: output file, 3: file ID
read_file = args[1]
rel_work_file = args[2]
file_id = args[3]

valid_lines = 0
possible_rel_works_count = [] 
with open(read_file, 'r+') as f:
  for counter in tqdm.tqdm(range(MAX_PROC), disable = True):
    line = f.readline();

    if not line:
        break
    paper_dict = json.loads(line)
    if paper_dict['body_text'] == []:
      continue

    check, blob = check_rel_work(paper_dict['body_text'])
    if check:
      valid_lines += 1
      unit = {}
      unit['paper_id'] = paper_dict['paper_id']
      unit['related_work'] = blob['text']

      candidate_sections = get_following_sections(paper_dict['body_text'])
      possible_rel_works = get_rel_work(candidate_sections, blob)

      unit['possible_rel_works'] = possible_rel_works
      possible_rel_works_count.append(len(possible_rel_works))

      with open(rel_work_file, 'a+') as o:
        o.write(str(json.dumps(ast.literal_eval(str(unit)))))
        o.write('\n')

print('Number of entries processed: ' + str(counter))
print('Number of entries with the Related Works sections: ' + str(valid_lines))
print('Average number of Related Work subsections: ' + str(np.mean(possible_rel_works_count)))
print('\n', flush = True)

# That's it
