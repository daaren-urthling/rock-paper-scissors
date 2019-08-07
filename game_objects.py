import json
from collections import namedtuple

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

class Action(object):
    def __init__(self, action, value):
        self.action = action
        self.value = value
    
    @staticmethod 
    def fromJson(jsonStr):
        obj = json2obj(jsonStr)
        if hasattr(obj, "action") and hasattr(obj, "value"):
            return Action(obj.action, obj.value)
        return None
    
    def toJson(self):
        return json.dumps(self.__dict__)