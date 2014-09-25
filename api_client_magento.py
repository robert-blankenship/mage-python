import suds
import pprint

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import


#I have no idea why this is necessary, but it is.
importedEncoding = Import('http://schemas.xmlsoap.org/soap/encoding/')
weirdFix = ImportDoctor(importedEncoding)

#The wsdl.
storeWSDL = "http://respectable-tobacco.com/index.php/api/soap/index/?wsdl"

client = Client(storeWSDL, doctor=weirdFix) 

user = 'python_client'
password = 'N28ju8O3L74gje9jZI91R2qQgVNv4ubs'

session = client.service.login(user, password)

categoryInfo = client.service.call(session, 'category.info', 8)
category = client.service.call(session, 'category.assignedProducts', 8)

print categoryInfo
print category
