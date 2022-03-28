import json

def ll_to_json(ll):
    """transform a list of lists to JSON (dict) representation"""
    d = {
        i: {
            j: data
            for j, data in enumerate(l)
        }
        for i, l in enumerate(ll)
    }
    return json.dumps(d)