import requests

#submit API request
x = "1"
resp = requests.get("https://localhost:8000/model", params={"x":x}, verify=False)

print(resp)