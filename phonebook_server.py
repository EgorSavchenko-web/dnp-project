import json
import os
import threading
import xmlrpc.server
import socketserver
from phonebook_logic import Phonebook


class ThreadedXMLRPCServer(socketserver.ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    pass


def main():
    server = ThreadedXMLRPCServer(('0.0.0.0', 8000), allow_none=True)
    server.register_instance(Phonebook())
    server.register_introspection_functions()
    print("Phonebook RPC server running on port 8000 (persistent storage enabled)")
    server.serve_forever()


if __name__ == '__main__':
    main()