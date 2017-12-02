import json

def load_locale(lang):
    with open('./strings.' + lang + '.json') as data_file: 
        return json.loads(data_file.read())
