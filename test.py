import json
json_file = open('settings.json')
json_data = json.load(json_file)

for key in json_data:  
    print(json_data[key])
