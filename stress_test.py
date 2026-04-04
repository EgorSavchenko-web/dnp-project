import xmlrpc.client
import concurrent.futures
import time

SERVER = "http://localhost:8000"

def delete_one(name):
    proxy = xmlrpc.client.ServerProxy(SERVER, allow_none=True)
    return proxy.delete(name)

def add_one(name, number):
    proxy = xmlrpc.client.ServerProxy(SERVER, allow_none=True)
    return proxy.add(name, number)

def edit_one(name, new_number):
    proxy = xmlrpc.client.ServerProxy(SERVER, allow_none=True)
    return proxy.edit(name, new_number)

def lookup_one(name):
    proxy = xmlrpc.client.ServerProxy(SERVER, allow_none=True)
    return proxy.lookup(name)

def delete_all(names):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(delete_one, name) for name in names]
        for f in concurrent.futures.as_completed(futures):
            f.result()

def add_all(items):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(add_one, name, number) for name, number in items]
        for f in concurrent.futures.as_completed(futures):
            f.result()

def edit_all(items):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(edit_one, name, new_number) for name, new_number in items]
        for f in concurrent.futures.as_completed(futures):
            f.result()

def lookup_all(names):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(lookup_one, name) for name in names]
        results = []
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())
        return results

def main():
    proxy = xmlrpc.client.ServerProxy(SERVER, allow_none=True)

    existing = proxy.list_all()
    existing_names = list(existing.keys())
    print(f"Found {len(existing_names)} existing entries. Deleting them...")
    start = time.perf_counter()
    delete_all(existing_names)
    delete_time = time.perf_counter() - start
    print(f"Deletion completed in {delete_time:.3f} seconds")

    entries = [(f"user_{i}", f"100{i}") for i in range(50)]
    print(f"\nAdding {len(entries)} entries...")
    start = time.perf_counter()
    add_all(entries)
    add_time = time.perf_counter() - start
    print(f"Addition completed in {add_time:.3f} seconds")

    edit_items = [(f"user_{i}", f"999{i}") for i in range(50)]
    print(f"\nEditing {len(edit_items)} entries...")
    start = time.perf_counter()
    edit_all(edit_items)
    edit_time = time.perf_counter() - start
    print(f"Editing completed in {edit_time:.3f} seconds")

    names = [f"user_{i}" for i in range(50)]
    print(f"\nLooking up {len(names)} entries...")
    start = time.perf_counter()
    lookup_results = lookup_all(names)
    lookup_time = time.perf_counter() - start
    print(f"Lookup completed in {lookup_time:.3f} seconds")

    print("\n=== STRESS TEST RESULTS ===")
    print(f"Delete time:   {delete_time:.3f} s")
    print(f"Add time:      {add_time:.3f} s")
    print(f"Edit time:     {edit_time:.3f} s")
    print(f"Lookup time:   {lookup_time:.3f} s")
    print("\nAll entries after test:")
    final_entries = proxy.list_all()
    for name, number in final_entries.items():
        print(f"  {name}: {number}")

if __name__ == "__main__":
    main()