import os
import json

def update_json(json_file, new_object, _):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
            print(data)

        if "questions" in data:
            data["questions"].extend(new_object["questions"])
        else:
            data["questions"] = new_object["questions"]

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        with open(json_file, 'w') as f:
            json.dump(new_object, f, indent=4)
