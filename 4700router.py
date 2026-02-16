import argparse, socket, time, json, select, struct, sys, math
from utils import Math
class Router:

    relations = {}
    sockets = {}
    ports = {}

    def __init__(self, asn, connections):
        print("Router at AS %s starting up" % asn)
        self.asn = asn
        for relationship in connections:
            port, neighbor, relation = relationship.split("-")

            self.sockets[neighbor] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sockets[neighbor].bind(('localhost', 0))
            self.ports[neighbor] = int(port)
            self.relations[neighbor] = relation
            self.send(neighbor, json.dumps({ "type": "handshake", "src": self.our_addr(neighbor), "dst": neighbor, "msg": {}  }))

    def our_addr(self, dst):
        quads = list(int(qdn) for qdn in dst.split('.'))
        quads[3] = 1
        return "%d.%d.%d.%d" % (quads[0], quads[1], quads[2], quads[3])

    def send(self, network, message):
        self.sockets[network].sendto(message.encode('utf-8'), ('localhost', self.ports[network]))

    def run(self):
        while True:
            socks = select.select(self.sockets.values(), [], [], 0.1)[0]
            for conn in socks:
                k, addr = conn.recvfrom(65535)
                message = json.loads(k.decode('utf-8'))
                msg_type = message["type"]

                srcif = None
                for sock in self.sockets:
                    if self.sockets[sock] == conn:
                        srcif = sock
                        break

                if msg_type == 'update':
                    self.update(message, scrif)
                elif msg_type == 'data':
                    self.data(message)
                elif msg_type == 'withdraw':
                    self.withdraw(message)
                elif msg_type == 'dump':
                    self.dump(message)

                print("Received message '%s' from %s" % (msg, srcif))
        return

    def update(self, message, srcif):
        payload = message["msg"]

        network = Math.ip_to_number(payload["network"])
        netmask = payload["netmask"]
        ASPath = payload["ASPath"]
        loalpref = payload["localpref"]
        origin = payload["origin"]
        selfOrigin = payload["selfOrigin"]

        self.table.append({
            "network": network, 
            "netmask": netmask, 
            "localpref": loalpref,
            "selfOrigin": selfOrigin,
            "ASPath": ASPath, 
            "origin": origin
            })

        foward_message = {}

        for neighbor in self.sockets:
            if neighbor != srcif:
                self.send(neighbor, json.dumps({ "type": "update", "src": self.our_addr(neighbor), "dst": neighbor, "msg": payload  }))

    def data(self, message, scrif): 
        pass 

    def withdraw(self, message, scrif): 
        pass

    def dump(self, message, scrif): 
        pass

    









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='route packets')
    parser.add_argument('asn', type=int, help="AS number of this router")
    parser.add_argument('connections', metavar='connections', type=str, nargs='+', help="connections")
    args = parser.parse_args()
    router = Router(args.asn, args.connections)
    router.run()