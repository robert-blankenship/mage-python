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

from suds.client import Client as SoapClient
from suds.xsd.doctor import ImportDoctor, Import
import suds

class MageClient():

	def __init__(self):
		self._init_suds()
		self._set_session()
		self._init_converter()

	def _init_suds(self):
		importedEncoding = Import('http://schemas.xmlsoap.org/soap/encoding/') #I have no idea why this is necessary, but it is.
		weirdFix = ImportDoctor(importedEncoding)
		#The wsdl.
		protocol = "http://"
		storeDomain = "www.lineapelle.com"
		storeWSDL = protocol + storeDomain + "/index.php/api/soap/index/?wsdl"

		self.client = SoapClient(storeWSDL, doctor=weirdFix)		

	def _set_session(self):
		user = 'Robert_ShopPad'
		password = '4d2e93fde5dd40ee6f15df304c6fb07b'
		self.session = self.client.service.login(user, password)
		self.service = self.client.service

	def _init_converter(self):
		self.kosherFactory = KosherFactory()

	def get(self, args):
		try:
			if args[0] == "configurable":
				rawOutput = self.client.service.call(self.session, "product.info", 9748)
				print dir(rawOutput)
				cleanOutput = self.kosherFactory.convert(rawOutput)
				return cleanOutput
				print "\npress 'q' to return to the main menu."
			else:
				rawOutput = self.service.call( self.session, *args)
				cleanOutput = self.kosherFactory.convert(rawOutput)
				return cleanOutput
				print "\npress 'q' to return to the main menu."
		except suds.WebFault as detail:
			print detail
			print "\npress 'q' to return to the main menu."

import pprint
p = pprint.PrettyPrinter()

import sys
def args():

	_args = list(sys.argv)
	_args.pop(0)

	if len(_args) > 1:
		if _args[1] in ['0','1','2','3','4','5','6','7','8','9','10']:
			_args[1] = int(_args[1])

	return _args

mageClient = MageClient()

product = mageClient.get( args() )

if product:
	p.pprint( product )



