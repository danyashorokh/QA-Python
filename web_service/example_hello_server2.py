from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger, String
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
import logging
from lxml import etree

d = {
    '1': 'Sasha',
    '2': 'Vasya',
    '3': 'Danya',
}

class EmpDemo(ServiceBase):

    @srpc(String, _returns=String) #UnsignedInteger
    def requestOperation(id):

        try:
            name_by_id = d[id]
            return "id = %s, name = %s" % (str(id), name_by_id)
        except Exception as e:
            print(e)
            return 'No such client id'




# http://127.0.0.1:8000/?wsdl
if __name__== '__main__':

    # logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    from wsgiref.simple_server import make_server

    app = Application([EmpDemo], tns='http://www.example.org',
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11()
                      )

    wsgi_app = WsgiApplication(app)


    server = make_server('127.0.0.1', 8001, wsgi_app)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server.serve_forever()
