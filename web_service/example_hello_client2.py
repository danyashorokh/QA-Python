from zeep import Client
from zeep.transports import Transport
from requests import Session
import sys

# import os
# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)

wsdl = 'C:/Oracle/Projects/example1/uml1/public_html/WEB-INF/wsdl/test.wsdl'
# wsdl = sys.path[0] + '/' + 'test.wsdl'

session = Session()

proxies = {"https": "https://dshorokh:Password30@fx-proxy:8080", "http":
    "http://dshorokh:Password30@fx-proxy:8080"}

session.proxies.update(proxies=proxies)
transport = Transport(session=session)
client = Client(wsdl=wsdl, transport=transport, strict=False)
#
# print(client.wsdl.dump())
# exit()

print(client.service.requestOperation(2))

exit()


# v.2
data = {'id': 1}

print(client.service.requestOperation(**data))
