import sys
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from phonebook_logic import Phonebook


class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def main():
    if len(sys.argv) > 1:
        try:
            host, port = sys.argv[1].split(":")
            port = int(port)
        except ValueError:
            print("Usage: python phonebook_server.py <host:port>")
            sys.exit(1)

    phonebook = Phonebook()
    server = ThreadedXMLRPCServer((host, port), allow_none=True)
    server.register_instance(phonebook)

    print(f"XML-RPC Phonebook server running on http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()