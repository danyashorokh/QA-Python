from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger, String
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
import logging
from lxml import etree

class HelloWorldService(ServiceBase):

    @srpc(String, UnsignedInteger, _returns=Iterable(String))

    def say_hello(name, times):
        for i in range(times):
            yield 'Hello, %s' % name


# http://127.0.0.1:8000/?wsdl
if __name__== '__main__':

    # logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    from wsgiref.simple_server import make_server

    app = Application([HelloWorldService], tns='spyne.examples.hello.http',
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11()
                      )

    wsgi_app = WsgiApplication(app)


    server = make_server('127.0.0.1', 8000, wsgi_app)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server.serve_forever()
