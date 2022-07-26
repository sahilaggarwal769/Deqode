import requests

Base="http://127.0.0.1:6000/"

headers= {
    "Accept": "*/*",
    "Content-Type": "application/json",
  }


data=[{"likes":120,"views":19,"name":"sahil"},
      {"likes":1020,"views":190,"name":"sahil1"},
      {"likes":10020,"views":1900,"name":"sahil2"}]

for i in range(len(data)):
    
    print("Adding new field value")
    response=requests.put(Base+"video/"+str(i),data[i],headers=headers)
    print(response.json())
    
input("Enter something")
print("Getting data with id 2")
response=requests.get(Base+"video/2")
print(response.json())

print("Aborting for getting wrong id")
response=requests.get(Base+"video/10")
print(response.json())

print("Updating field values")
response=requests.patch(Base+"video/2",{"views":1000})
print(response.json())

print("Deleting data with id 2 ")
response=requests.delete(Base+"video/2")
print(response.json())

print("Aborting for deleting wrong id")
response=requests.delete(Base+"video/10")
print(response.json())

