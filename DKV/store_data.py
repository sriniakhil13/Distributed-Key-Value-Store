import time
import os
import json

class DataStore:
    def __init__(self, key='0', value='0'):
        self.key = key
        self.value = value

    def _get(self, key):
        with open("db.json", 'r') as db:
            json_decoded = json.load(db)
            try:
                value = json_decoded[key]["value"]
                return json_decoded[key]
            except:
                return "No key found !"
    def get(self,key):
        with open("db.json", 'r') as db:
            json_decoded = json.load(db)
            try:
                value = json_decoded[key]["value"]
                expiry_time = json_decoded[key]["expire_time"]
                if expiry_time !="":
                    if int(str(expiry_time)) > int(str(round(time.time()))):
                        return str(value)
                    else:
                        return "Expired value !"
                else:
                    return str(value)

            except:
                return "No key found !"

    def set(self,key,value):
        with open("db.json", 'r') as db:
            data = json.load(db)
            temp_dict = dict()
            inner_temp_dict = dict()
            inner_temp_dict["value"] = value
            inner_temp_dict["record_modified_time"] = str(round(time.time()))
            inner_temp_dict["expire_time"] =""
            temp_dict[key] = inner_temp_dict
            data.update(temp_dict)
        with open("db.json", 'w') as db:
            json.dump(data, db)
        return "Done"

    def expire(self,key,seconds):
        with open("db.json", 'r') as db:
            json_decoded = json.load(db)
        with open("db.json", 'w') as db:
            try:
                value = json_decoded[key]["value"]
                json_decoded[key]["expire_time"] = str(int(round(time.time()))+int(seconds))
                json_decoded[key]["record_modified_time"] = str(round(time.time()))
                json.dump(json_decoded, db)
                return "Done !"
            except:
                return "Key Not found !"





'''
{
    "01": {
        "value": "tree",
        "expire_time":"",
        "record_modified_time":""
    }
}
'''