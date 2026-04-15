import json
import os
import threading

class Phonebook:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.storage_file = os.path.join(script_dir, "phonebook.json")
        self.lock = threading.RLock()
        self.data = self._load()

    def _load(self):
        """Load data from JSON file on startup."""
        if not os.path.exists(self.storage_file):
            return {}
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _atomic_write(self):
        """
        Write current data to a temporary file, then atomically replace
        the main file. This prevents corruption if the process crashes
        during write.
        """
        tmp_file = self.storage_file + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file, self.storage_file)

    def add(self, name, number):
        with self.lock:
            if name in self.data:
                return f"ERROR: contact '{name}' already exists"
            self.data[name] = number
            self._atomic_write()
            return f"OK: added {name}"

    def edit(self, name, new_number):
        with self.lock:
            if name not in self.data:
                return f"ERROR: contact '{name}' not found"
            self.data[name] = new_number
            self._atomic_write()
            return f"OK: updated {name}"

    def delete(self, name):
        with self.lock:
            if name not in self.data:
                return f"ERROR: contact '{name}' not found"
            del self.data[name]
            self._atomic_write()
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