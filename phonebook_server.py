import json
import os
import threading
import xmlrpc.server
import socketserver

class Phonebook:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.storage_file = os.path.join(script_dir, "phonebook.json")
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.storage_file):
            return {}
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def add(self, name, number):
        with self.lock:
            if name in self.data:
                return f"ERROR: contact '{name}' already exists"
            self.data[name] = number
            self._save()
            return f"OK: added {name}"

    def edit(self, name, new_number):
        with self.lock:
            if name not in self.data:
                return f"ERROR: contact '{name}' not found"
            self.data[name] = new_number
            self._save()
            return f"OK: updated {name}"

    def delete(self, name):
        with self.lock:
            if name not in self.data:
                return f"ERROR: contact '{name}' not found"
            del self.data[name]
            self._save()
            return f"OK: deleted {name}"

    def lookup(self, name):
        with self.lock:
            number = self.data.get(name)
            if number is None:
                return f"ERROR: '{name}' not found"
            return number

    def list_all(self):
        with self.lock:
            return dict(self.data)

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