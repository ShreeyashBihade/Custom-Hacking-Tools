import requests # type: ignore

# GET
'''
params = {
    "name" : "Mike",
    "age" : "25"
}

response = requests.get("https://httpbin.org/get", params=params) # Same as https://httpbin.org/get?name=Mike&age=25
print(response.url)


res_json = response.json()
del res_json['origin']
print(res_json)
'''
# POST
'''
payload = {
    "name" : "Mike",
    "age" : 25
}

response = requests.post("https://httpbin.org/post", data=payload)
print(response.url)

res_json = response.json()
del res_json['origin']
print(res_json)
'''

# Error Handling
response = requests.get("https://httpbin.org/status/404")

if response.status_code == requests.codes.not_found:
    print("Not Found")
else:
    print(response.text)
