from tornado.options import options

from .server import RemoteServer

def startserver():
    fonera = RemoteServer()
    # FIXME single threaded?
    #fonera.bind(options.fonera_port, options.fonera_address)
    #fonera.start(0)  # Forks multiple sub-processes
    fonera.listen(options.remote_port, options.fonera_address)
