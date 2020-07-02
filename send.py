import requests

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkzNzEzOTM3LCJqdGkiOiIyOWYwMTZhOTEwYzQ0YTc0YWMyZTUxYTU1MDAxYjljYyIsInVzZXJfaWQiOjF9.D-A4eBE5t2pPQ3b6N0vZbIaetNQx7nayyxBrWQcrHeQ'

r = requests.get(" http://127.0.0.1:8000/paradigms/", headers = headers)

print(r.text)