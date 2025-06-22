import json

class JSONParser:
    def __init__(self):
        self.parsed_event = {}
    
    def _expand_dict(self, key, val):
        expanded_dict = {}
        for k, v in val.items():
            expanded_dict[key+"_"+k] = v
            print(expanded_dict)
        return expanded_dict
        
    def parse(self, event):
        try:
            self.parsed_event = json.loads(event)
        except json.JSONDecodeError as e:
            print("Invalid JSON...")
        for key, val in list(self.parsed_event.items()):
            if isinstance(val, dict):
                self.parsed_event.update(self._expand_dict(key, val))
                self.parsed_event.pop(key)
        print(self.parsed_event)
        
if __name__ == "__main__":
    # msg = r'''{"key": "value"}'''
    # msg = r'''{"key1":true,"key2":false,"key3":null,"key4":"value","key5":101}'''
    msg = r'''a{"key":"value","key-n":101,"key-o":{"a": 1, "b": "b"},"key-l":[]}'''
    parser = JSONParser()
    parser.parse(msg)