import xmlrpc.client
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <server_url>")
        print("Example: python client.py http://localhost:8000")
        sys.exit(1)

    proxy = xmlrpc.client.ServerProxy(sys.argv[1], allow_none=True)

    while True:
        cmd = input("\n> ").strip().split()
        if not cmd:
            continue
        op = cmd[0].lower()
        if op == 'add' and len(cmd) == 3:
            print(proxy.add(cmd[1], cmd[2]))
        elif op == 'edit' and len(cmd) == 3:
            print(proxy.edit(cmd[1], cmd[2]))
        elif op == 'delete' and len(cmd) == 2:
            print(proxy.delete(cmd[1]))
        elif op == 'lookup' and len(cmd) == 2:
            result = proxy.lookup(cmd[1])
            print(result if result.startswith("ERROR") else f"Phone: {result}")
        elif op == 'list':
            data = proxy.list_all()
            for name, num in data.items():
                print(f"{name}: {num}")
        elif op == 'exit':
            break
        else:
            print("Commands: add NAME NUMBER | edit NAME NEW_NUMBER | delete NAME | lookup NAME | list | exit")

if __name__ == '__main__':
    main()