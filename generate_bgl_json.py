import pandas as pd
import json
import re
import sys
sys.path.append('.')
from utils import REGEX_PATTERN

def generate():
    df = pd.read_csv('dataset/BGL/BGL.log_structured.csv', nrows=1000) # just use 1000 rows for few-shot
    out_data = []
    
    with open('dataset/BGL/dataset.json', 'w') as f:
        for idx, row in df.iterrows():
            log = row['Content']
            entities = []
            tags = []
            for tag, pat in REGEX_PATTERN.items():
                ans = re.findall(pat, log + ' ')
                if ans:
                    for phrase in ans:
                        if isinstance(phrase, str):
                            entities.append(phrase)
                            tags.append(tag)
                        elif isinstance(phrase, tuple):
                            p = min(list(phrase), key=len)
                            entities.append(p)
                            tags.append(tag)
            
            # Write line by line
            record = {
                "logex:example": log,
                "logex:hasParameterList": entities,
                "logex:hasNERtag": tags
            }
            f.write(json.dumps(record) + '\n')

if __name__ == '__main__':
    generate()
