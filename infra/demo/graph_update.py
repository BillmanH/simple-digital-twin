import os
import json
import pandas as pd

class dtdl:
  def __init__(self, j):
    self.input_dict = j
    self.template = self.read_json()
    if 'class' in j.keys():
      self.class_name = j['class']
    else:
      print('No class name found in input dictionary')
    self.name = j['name']
  def read_json(self):
    print(os.path.join('infra','demo','dtdl',self.input_dict['class']+'.json'))
    return json.load(
      open(os.path.join('infra','demo','dtdl',self.input_dict['class']+'.json').read()
      ))
  def __repr__(self):
    return(f"<dtdl object - {self.name}>")

    
df = pd.read_csv(os.path.join('.','infra','demo','equipment.csv'))
dtdls = [dtdl(j) for j in df.to_dict('records')]
d = dtdls[0]