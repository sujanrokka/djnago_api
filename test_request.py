import requests
# response =requests.request("GET",'https://dummyjson.com/products')
# data=response.json()
# products=data['products']
# for product in products:
#     print["PRODUCT",product['title']]
# # print(data['products'][0]['title'])
credentials={
    'username':'admin',
    'password':'admin'
}
response=requests.request("POST",'http://localhost:8000/api-token-auth/',json=credentials)
data=response.json()
print(data)
token='937b11e4e951237f5b955c804f7aef356727e0a3'

headers={
    'Authorization':'Token '+token
}

response=requests.request("GET",'http://localhost:8000/recipe/recipes/',headers=headers)
data=response.json()
print(data)
