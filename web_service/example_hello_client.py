from zeep import Client
from zeep.transports import Transport
from requests import Session

wsdl = 'http://127.0.0.1:8000/?wsdl'

session = Session()

proxies = {"https": "https://dshorokh:Password30@fx-proxy:8080", "http":
    "http://dshorokh:Password30@fx-proxy:8080"}

session.proxies.update(proxies=proxies)
transport = Transport(session=session)
client = Client(wsdl=wsdl, transport=transport, strict=False)


print(client.wsdl.dump())
exit()
# v.1
print(client.service.say_hello('Danya', 3))


# # v.2
# data = {'name': 'Vasya',
#         'times': 4}
#
# print(client.service.say_hello(**data))
