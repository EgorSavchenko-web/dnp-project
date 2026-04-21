import xmlrpc.client
import time
import statistics

SERVER_URL = "http://192.168.177.4:8000"
N = 20

proxy = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)

def measure(name, func, repeats=N):
    times = []

    for _ in range(repeats):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append((end - start) * 1000)

    print(f"\n{name}")
    print(f"min: {min(times):.2f} ms")
    print(f"avg: {statistics.mean(times):.2f} ms")
    print(f"max: {max(times):.2f} ms")

try:
    proxy.add("bench_user", "123456")
except:
    pass

measure("lookup latency", lambda: proxy.lookup("bench_user"))
measure("list latency", lambda: proxy.list_all())
measure("edit latency", lambda: proxy.edit("bench_user", "999999"))
measure("delete latency", lambda: proxy.delete("bench_user"))

try:
    proxy.delete("bench_add")
except:
    pass

measure("add latency", lambda: proxy.add("bench_add", "111111"), repeats=10)