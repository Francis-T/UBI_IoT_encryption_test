from sys import argv

import defs
from node import NodeServer, NodeClient

class NodeRunner():
    def __init__(self, node_type=defs.NODE_UNKNOWN, 
                       enc_mode=defs.ENC_MODE_DEFAULT):
        self.node_type = node_type
        self.encryption_mode = enc_mode
        return

    def log(self, message):
        print("[NodeRunner] ()".format(message))
        return

    def run(self):
        if self.node_type == defs.NODE_UNKNOWN:
            self.log("Node type not specified")
            return

        # Initialize the node
        node = None
        if self.node_type == defs.NODE_CLIENT:
            node = NodeClient(self.encryption_mode)

        elif self.node_type == defs.NODE_SERVER:
            node = NodeServer(self.encryption_mode)

        # Run the node
        node.run()

        return

if __name__ == "__main__":
    node_type = argv[1]
    enc_mode  = argv[2]
    print(node_type + " " + enc_mode)
    NodeRunner(node_type=node_type,enc_mode=enc_mode).run()


