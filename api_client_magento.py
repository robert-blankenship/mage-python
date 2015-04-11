import suds
import pprint

p = pprint.PrettyPrinter()

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

#I have no idea why this is necessary, but it is.
importedEncoding = Import('http://schemas.xmlsoap.org/soap/encoding/')
weirdFix = ImportDoctor(importedEncoding)

#The wsdl. Replace "respectable-tobacco.com" with your domain.
storeWSDL = "http://respectable-tobacco.com/index.php/api/soap/index/?wsdl"

client = Client(storeWSDL, doctor=weirdFix) 

user = 'python_client' #your username, need to create this in magento.
password = 'N28ju8O3L74gje9jZI91R2qQgVNv4ubs' #your password for the user.

print 'starting session'
session = client.service.login(user, password)

print 'getting catalog info'
# categoryInfo = client.service.call(session, 'category.tree')
# category = client.service.call(session, 'category.assignedProducts', 5)
product = client.service.call(session, 'product.info', 36)

class kosherFactory():

	def convert_list(self, obj):
		newObj = list()

		if len(obj) == 1:
			return self.convert(obj[0])

		for elem in obj:
			newObj.append(self.convert(elem))

		return newObj		

	def convert_faux_obj(self, item):
		newObj = {}
		
		for elem in item:

			key = str(self.convert(elem.key))
			value = self.convert(elem.value)

			newObj[key] = value

		return newObj

	def convert(self, obj):
		if type(obj) is list:
			return self.convert_list(obj)

		if type(obj) is int:
			return obj

		if type(obj) is str:
			return obj

		if type(obj) is dict:
			return obj

		if obj is None:
			return None

		if 'item' in dir(obj):
			return self.convert_faux_obj(obj.item)
		else:
			return obj


kosherFact = kosherFactory()

out = kosherFact.convert(product)

p.pprint(out)
