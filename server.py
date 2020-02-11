#!/usr/bin/env python3
from twisted.internet import protocol, reactor, endpoints
from threading import Thread
clients = []
lol = ""


class Echo(protocol.Protocol):
    def connectionMade(self):
        clients.append(self)

    def connectionLost(self, reason):
        clients.pop(clients.index(self))


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print(f"connection from, {addr.host} on port, {addr.port}")
        Echo.addr = addr
        return Echo()


def thr_test():
    n = ""
    while n != "exit":
        n = input("> ")
        if len(clients) > 0:
            clients[0].transport.write(str.encode(n + "\n"))


endpoints.serverFromString(reactor, "tcp:42069").listen(EchoFactory())
thr1 = Thread(target=thr_test)
thr1.start()

reactor.run()
