import json
import requests

hola = requests.get("http://127.0.0.1:5000/", data={"name": ["foo", "poo", "koo"]})
print("hola")