"""qui definisco tutte le funzioni utili per lavorare con i json in modo veloce"""

import json
"""questa funzione mi consente di creare un File Json
-input : dataset, path"""
def createJson(data:[],path: str):
    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = []
"""La seguente funzione mi consente di associare un Json ad una lista
 -input: path del Json"""
def loadJson(path: str):
    with open(path, encoding='utf-8') as f:

        data =json.load(f)
    return data
"""la seguente funzione mi consente di ricavare un voce all'interno del json, comunque essa sia annidata"""
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values