import xmlrpc.client
import threading
import time
import random
import sys
from datetime import datetime

SERVER_URL = "http://localhost:8000"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {msg}", flush=True)

def rpc_call(func, *args):
    try:
        proxy = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)
        method = getattr(proxy, func)
        result = method(*args)
        log(f"CALL {func}{args} -> {result[:50] if result else result}")
        return result
    except Exception as e:
        log(f"ERROR {func}{args}: {e}")
        return None

def test_concurrent_edit_same_contact():
    print("\n=== TEST 1: Concurrent edit of the SAME contact ===")
    contact_name = "conflict_test"
    rpc_call("add", contact_name, "000")
    N = 20
    results = []
    lock = threading.Lock()

    def edit_worker(worker_id, new_number):
        time.sleep(random.uniform(0, 0.02))
        resp = rpc_call("edit", contact_name, new_number)
        with lock:
            results.append((worker_id, new_number, resp))

    threads = []
    for i in range(N):
        number = f"{1000 + i}"
        t = threading.Thread(target=edit_worker, args=(i, number))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    final = rpc_call("lookup", contact_name)
    print(f"\nFINAL value for '{contact_name}': {final}")
    print(f"Total successful edits: {sum(1 for _,_,r in results if r and 'OK' in r)}")
    rpc_call("delete", contact_name)
    print("Test 1 finished.\n")

def test_mixed_concurrent_ops():
    print("=== TEST 2: Mixed concurrent add/lookup/edit/delete on different keys ===")
    base_names = [f"mixed_{i}" for i in range(10)]
    for name in base_names:
        rpc_call("add", name, "initial")

    operations = [
        ("add", lambda: (f"new_{random.randint(1000,9999)}", str(random.randint(100000,999999)))),
        ("lookup", lambda: (random.choice(base_names + [f"new_{i}" for i in range(100) if random.random()>0.7]),)),
        ("edit", lambda: (random.choice(base_names), str(random.randint(100000,999999)))),
        ("delete", lambda: (random.choice(base_names),)),
    ]
    N_REQUESTS = 50
    threads = []
    results = []

    def worker(req_id):
        time.sleep(random.uniform(0, 0.01))
        func, arg_gen = random.choice(operations)
        args = arg_gen()
        resp = rpc_call(func, *args)
        with threading.Lock():
            results.append((req_id, func, args, resp))

    for i in range(N_REQUESTS):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    final_list = rpc_call("list_all")
    print(f"\nFinal phonebook size: {len(final_list) if final_list else 0}")
    print(f"Total requests: {N_REQUESTS}, successful among logged: {sum(1 for r in results if r[3] and 'ERROR' not in r[3])}")
    for name in base_names:
        rpc_call("delete", name)
    print("Test 2 finished.\n")

def test_concurrent_add_delete_same():
    print("\n=== TEST 3: Concurrent add and delete on same key ===")
    key = "racy_key"
    rpc_call("delete", key)

    def adder():
        time.sleep(0.005)
        return rpc_call("add", key, "111")

    def deleter():
        time.sleep(0.010)
        return rpc_call("delete", key)

    t1 = threading.Thread(target=adder)
    t2 = threading.Thread(target=deleter)
    t1.start(); t2.start()
    t1.join(); t2.join()

    final = rpc_call("lookup", key)
    print(f"After concurrent add+delete: lookup('{key}') -> {final}")
    rpc_call("delete", key)
    print("Test 3 finished.\n")

if __name__ == "__main__":
    try:
        test_proxy = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)
        test_proxy.list_all()
    except Exception as e:
        print(f"Cannot connect to server at {SERVER_URL}: {e}")
        sys.exit(1)

    test_concurrent_edit_same_contact()
    test_mixed_concurrent_ops()
    test_concurrent_add_delete_same()
    print("\nAll tests done. Check logs above for any ERROR or lost update.")