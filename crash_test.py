import os
import sys
import time
import json
import signal
import subprocess
import tempfile
import xmlrpc.client
from pathlib import Path

SERVER_SCRIPT = "phonebook_server.py"
SERVER_URL = "http://localhost:8000"
STORAGE_FILE = "phonebook.json"
TMP_FILE = STORAGE_FILE + ".tmp"

def cleanup():
    for f in [STORAGE_FILE, TMP_FILE]:
        if os.path.exists(f):
            os.remove(f)

def start_server():
    return subprocess.Popen([sys.executable, SERVER_SCRIPT, "localhost:8000"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def wait_for_server(timeout=3):
    start = time.time()
    while time.time() - start < timeout:
        try:
            proxy = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)
            proxy.list_all()
            return True
        except:
            time.sleep(0.2)
    return False

def get_storage_state():
    if not os.path.exists(STORAGE_FILE):
        return None
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def inject_delay_in_server():
    logic_path = Path(__file__).parent / "phonebook_logic.py"
    backup_path = logic_path.with_suffix(".py.bak")
    if not backup_path.exists():
        import shutil
        shutil.copy(logic_path, backup_path)

    with open(logic_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "def _atomic_write(self):" in content:
        new_content = content.replace(
            "        os.replace(tmp_file, self.storage_file)",
            "        time.sleep(0.5)\n        os.replace(tmp_file, self.storage_file)"
        )
        if "import time" not in new_content:
            new_content = "import time\n" + new_content
        with open(logic_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def restore_server_code():
    backup_path = Path(__file__).parent / "phonebook_logic.py.bak"
    original = Path(__file__).parent / "phonebook_logic.py"
    if backup_path.exists():
        import shutil
        shutil.copy(backup_path, original)
        backup_path.unlink()

def test_crash_during_write():
    print("=== CRASH RECOVERY TEST ===")
    cleanup()
    inject_delay_in_server()

    server_proc = start_server()
    if not wait_for_server():
        print("Server failed to start")
        restore_server_code()
        sys.exit(1)

    proxy = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)
    print("Sending 'add crash_test 12345'...")
    import threading
    result_holder = [None]

    def do_add():
        try:
            result_holder[0] = proxy.add("crash_test", "12345")
        except Exception as e:
            result_holder[0] = f"EXCEPTION: {e}"

    t = threading.Thread(target=do_add)
    t.start()
    time.sleep(0.2)
    print("Killing server process during atomic write...")
    server_proc.kill()
    server_proc.wait()
    t.join(timeout=1)

    print(f"Client result (if any): {result_holder[0]}")
    print("Checking storage file integrity...")
    state_before_restart = get_storage_state()
    print(f"Storage after crash: {state_before_restart}")

    print("Restarting server...")
    server_proc2 = start_server()
    if not wait_for_server():
        print("Server restart failed")
        restore_server_code()
        sys.exit(1)

    state_after_restart = get_storage_state()
    print(f"Storage after restart: {state_after_restart}")

    if state_after_restart is None:
        print("FAIL: phonebook.json is corrupt or missing after crash!")
    else:
        has_entry = "crash_test" in state_after_restart
        print(f"Entry 'crash_test' present: {has_entry}")
        print("SUCCESS: Storage file is valid JSON and consistent.")
    cleanup()
    restore_server_code()
    server_proc2.terminate()
    server_proc2.wait()

if __name__ == "__main__":
    test_crash_during_write()