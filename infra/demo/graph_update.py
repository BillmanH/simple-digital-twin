import os
import json
import pandas as pd
import numpy as np

from ...connectors import cmdbgraph


# TODO: Read these config vars from a config file
# Length of characters of the UUID
DTDL_ID_LENGTH = 13

class TemplateNotFoundError(Exception):
    print("no template was found with the correct name in the infra folder")
    pass



class dtdl:
    def __init__(self, j):
        # Template stuff
        self.DTDL_ID_LENGTH = DTDL_ID_LENGTH

        print(f"creating model object for {j.get('name')}, from template {j.get('class')}")
        self.input_dict = j
        # Loading the template files
        self.template = self.read_json(self.input_dict['class'])
        if self.template.get('extends'):
            print(f"     * Template {self.template.get('@id','MissingID')} is extended from template: {self.template.get('extends')}")
            # TODO: extended templates will need a more robust process that can recursively collect from multiple extensions
            #       the current model just allows one extension. Createing a looping `get_extensions` function that returns an array of extention templates should do it.
            self.extensions = [self.read_json(self.template['extends'].replace('dtmi:com:adt:dtsample:','').replace(';1',''))]
        else:
            self.extensions = []
        if 'class' in j.keys():
            self.label = j['class']
        else:
            print('No class name found in input dictionary')

        # Building the model object to be uploaded
        self.model = {'name':'model not extablished'}
        self.build_model()
        self.name = j['name'] 

    def uuid(self):
        return "dtid:" + "".join([str(i) for i in np.random.choice(range(10), self.DTDL_ID_LENGTH)])
    
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
        # Attach a GUID for the object as dtdlid
        self.model['dtid'] = self.uuid()
        self.model['label'] = self.label

        # CosmosDB doesnt support nested objects very well, so we flattening the structure for the graph. 
        for item in self.model['contents']:
            if item['@type'] == "Property":
                self.model[item['name']] = 'default: ' + item['displayName']
        self.model.pop('contents')
        
    def __repr__(self):
        return(f"<dtdl object - {self.label}:{self.name}>")


# c = CosmosdbClient()

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