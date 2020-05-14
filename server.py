#!/usr/bin/env python3
from twisted.internet import protocol, reactor, endpoints
from threading import Thread
from socket import gethostbyaddr
clients = []
port = "22443"
con_id = None


def list_connections():
    for c in range(len(clients)):
        print(f"{c}: {clients[c].addr.host} {clients[c].hostname}\n")


class Echo(protocol.Protocol):
    def connectionMade(self):
        clients.append(self)

    def dataReceived(self, data):
        if data.decode('utf-8').split()[0] == "hostname":
            self.hostname = data.decode('utf-8').split()[1]
        else:
            if con_id in range(len(clients)):

                print(f"\r{self.hostname}: \n" + data.decode('utf-8') +
                      f"\n{clients[con_id].hostname}> ", end='')
            else:
                print(f"\r{self.hostname}: \n" + "\r" +
                      data.decode('utf-8') + f"\n> ", end='')

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
    con_id = None
    while n != "exit":
        try:
            n = input(f"{clients[con_id].hostname}> ")
        except:
            n = input(f"> ")
        if len(clients) < 1:
            print("no connections")
            continue
        if n == "":
            print("please enter a command")
            continue

        if n == "clients":
            list_connections()
        elif n.split()[0] == "select":
            try:
                if int(n.split()[1]) not in range(len(clients)):
                    print("Client not found")
                else:
                    con_id = int(n.split()[1])
            except:
                print("please enter a valid number")
        else:
            if con_id not in range(len(clients)):
                for i in range(len(clients)):
                    clients[i].transport.write(str.encode(n) + b"\n")
            else:
                clients[con_id].transport.write(str.encode(n) + b"\n")


endpoints.serverFromString(reactor, f"tcp:{port}").listen(EchoFactory())
thr1 = Thread(target=thr_test)
thr1.start()

reactor.run()
