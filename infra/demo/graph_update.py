import os
import json
import pandas as pd

base_models = []


class TemplateNotFoundError(Exception):
    print("no template was found with the correct name in the infra folder")
    pass


class dtdl:
  def __init__(self, j):
    print(f"creating model object for {j.get('name')}, from template {j.get('class')}")
    self.input_dict = j
    self.template = self.read_json(self.input_dict['class'])
    if self.template.get('extends'):
       print(f"     * Template {self.template.get('@id','MissingID')} is extended from template: {self.template.get('extends')}")
       # TODO: extended templates will need a more robust process that can recursively collect from multiple extensions
       #       the current model just allows one extension. Createing a looping `get_extensions` function that returns an array of extention templates should do it.
       self.extensions = [self.read_json(d.template['extends'].replace('dtmi:com:adt:dtsample:','').replace(';1',''))]
    else:
       self.extensions = []
    if 'class' in j.keys():
      self.class_name = j['class']
    else:
      print('No class name found in input dictionary')
    self.build_model()
    self.name = j['name'] 

  def read_json(self,filename):
    # get load the template, and let the user know if the file is not found.
    path = os.path.join('.','dtdl',filename + '.json')
    try:
        template = json.load(open(path))
    except:
        print(f'ERROR: no file found at : {path}')
        TemplateNotFoundError()
    return template
  
  def build_model(self):
    model = {}
    for ext in self.extensions:
        # TODO: Process is not truly recursive. This will need to be updated to allow recursively building extensions
        for k in ext.keys():
           model[k] = ext[k]
    # Finally, load the template for the object
    for t in self.template.keys():
       model[t] = self.template[t]
    self.model = model
         
  
  def __repr__(self):
    return(f"<dtdl object - {self.name}>")


try:    
    df = pd.read_csv(os.path.join('.','infra','demo','equipment.csv'))
except:
    df = pd.read_csv(os.path.join('equipment.csv'))

dtdls = [dtdl(j) for j in df.to_dict('records')]
d = dtdls[0]


j = df.to_dict('records')[0]
dtdl(j)


json.load(open(os.path.join('.','dtdl',j['class']+'.json')))

d.template['extends'].replace('dtmi:com:adt:dtsample:','').replace(';1','')