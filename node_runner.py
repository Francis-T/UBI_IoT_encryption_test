from sys import argv

import defs
from node_client import NodeClient
from node_server import NodeServer

class NodeRunner():
    def __init__(self, node_type=defs.NODE_UNKNOWN, 
                       enc_mode=defs.ENC_MODE_DEFAULT,
                       max_buf_size=defs.MAX_MSG_BUF,
                       data_size=defs.DEFAULT_DATA_SIZE):

        self.node_type = node_type
        self.encryption_mode = enc_mode
        self.max_buf_size = int(max_buf_size)
        self.data_size = int(data_size)
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
            node = NodeClient( enc_mode=self.encryption_mode,
                               max_buf_size=self.max_buf_size,
                               data_size=self.data_size )

        elif self.node_type == defs.NODE_SERVER:
            node = NodeServer( enc_mode=self.encryption_mode,
                               max_buf_size=self.max_buf_size,
                               data_size=self.data_size )

        # Run the node
        node.run()

        return

if __name__ == "__main__":
    node_type = argv[1]
    enc_mode  = argv[2]
    data_size = argv[3] if len(argv) >= 4 else str(defs.DEFAULT_DATA_SIZE)
    buf_size  = argv[4] if len(argv) >= 5 else str(defs.MAX_MSG_BUF)
    print(node_type + " " + enc_mode + " " + data_size + " " + buf_size)
    NodeRunner(node_type=node_type, enc_mode=enc_mode, max_buf_size=buf_size, data_size=data_size).run()


