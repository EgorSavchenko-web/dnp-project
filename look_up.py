import timeit
setup = """
import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://localhost:8000", allow_none=True)
proxy.add("test", "000")
"""
stmt = 'proxy.lookup("test")'
latency = timeit.timeit(stmt, setup=setup, number=1000) / 1000
print(f"Average lookup latency: {latency*1000:.2f} ms")