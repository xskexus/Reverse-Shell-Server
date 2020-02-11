#!/usr/bin/env python3
from twisted.internet import protocol, reactor, endpoints
from threading import Thread
from socket import gethostbyaddr
clients = []
lol = ""


def list_connections():
    for c in range(len(clients)):
        print(f"{c}: {clients[c].addr.host}\n")


class Echo(protocol.Protocol):
    def connectionMade(self):
        clients.append(self)

    def dataReceived(self, data):
        print(data.decode('utf-8') + f"\n> ", end='')

    def connectionLost(self, reason):
        clients.pop(clients.index(self))


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print(
            f"\rconnection from, {addr.host} on port, {addr.port}\n> ", end='')
        Echo.addr = addr
        return Echo()


def thr_test():
    n = ""
    con_id = 0
    while n != "exit":
        n = input(f"> ")
        if len(clients) < 1:
            print("no connections")
            continue
        if n == "clients":
            list_connections()
        elif n.split()[0] == "select":
            try:
                con_id = int(n.split()[1])
            except:
                print("please enter a valid number")
        else:
            clients[con_id].transport.write(str.encode(n))


endpoints.serverFromString(reactor, "tcp:42069").listen(EchoFactory())
thr1 = Thread(target=thr_test)
thr1.start()

reactor.run()
