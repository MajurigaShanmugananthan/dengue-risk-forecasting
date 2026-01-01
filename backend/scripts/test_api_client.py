import requests
print(requests.get("http://127.0.0.1:5000/api/health").json())
print(requests.get("http://127.0.0.1:5000/api/moh-areas").json())
print(requests.get("http://127.0.0.1:5000/api/risk/1").json())
