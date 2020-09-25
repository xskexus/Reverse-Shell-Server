#!/usr/bin/env python3
from twisted.internet import protocol, reactor, endpoints
from threading import Thread
from socket import gethostbyaddr
# preparing the list of clients
clients = []
# setting port to listen for connections on
port = "22443"
# setting variable to be used by function
con_id = None

# function to handle listing connections and their ids


def list_connections():
    for c in range(len(clients)):
        print(f"{c}: {clients[c].addr.host} {clients[c].hostname}\n")

# Handling connection and disconnection and handling their respective lists


class Echo(protocol.Protocol):
    # adding clients to the list of clients
    def connectionMade(self):
        clients.append(self)
    # receiving data from a client

    def dataReceived(self, data):
        # setting the hostname
        if data.decode('utf-8').split()[0] == "hostname":
            self.hostname = data.decode('utf-8').split()[1]
        # still display command line when no hostname is supplied
        else:
            if con_id in range(len(clients)):

                print(f"\r{self.hostname}: \n" + data.decode('utf-8') +
                      f"\n{clients[con_id].hostname}> ", end='')
            else:
                print(f"\r{self.hostname}: \n" + "\r" +
                      data.decode('utf-8') + f"\n> ", end='')

    def connectionLost(self, reason):
        clients.pop(clients.index(self))


# Receiving connections and forwarding them to the Echo function
class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print(
            f"\rconnection from, {addr.host} on port, {addr.port}\n> ", end='')
        Echo.addr = addr
        return Echo()

# command line


def thread_test():
    n = ""
    con_id = None
    # adds the exit command
    while n != "exit":
        # if there is no client it hides the hostname
        try:
            n = input(f"{clients[con_id].hostname}> ")
        except:
            n = input(f"> ")
        # if there are no clients don't process commands
        if len(clients) < 1:
            print("no connections")
            continue
        # if there isn't a command ask for a command
        if n == "":
            print("please enter a command")
            continue
        # if the command is clients list the connections
        if n == "clients":
            list_connections()
        # select a client
        elif n.split()[0] == "select":
            try:
                # if the client isn't found reply client not found
                if int(n.split()[1]) not in range(len(clients)):
                    print("Client not found")
                # but if it is correct set the connection id to the client
                else:
                    con_id = int(n.split()[1])
            # if the supplied number isn't valid then exit
            except:
                print("please enter a valid number")
        # if not a command that can be handled by the server send it to the client
        else:
            # if no client is selected send it to them all
            if con_id not in range(len(clients)):
                for i in range(len(clients)):
                    clients[i].transport.write(str.encode(n) + b"\n")
            # send it to the client selected
            else:
                clients[con_id].transport.write(str.encode(n) + b"\n")


# starting listening
endpoints.serverFromString(reactor, f"tcp:{port}").listen(EchoFactory())
thr1 = Thread(target=thread_test)
thr1.start()

reactor.run()
