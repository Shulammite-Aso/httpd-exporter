import requests
from prometheus_client import start_http_server, Counter
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY

APP_URL = "https://80-shulammitea-httpservere-rrmmdge1rcs.ws-eu63.gitpod.io/server-status/?auto"

def get_metrics():
    resp = requests.get(url=APP_URL)
    byte_data = resp.content

    data = str(byte_data, 'UTF-8')

    lines = data.split('\n')

    return lines

def split_pair(pair=""):
    key_and_value = pair.split(':')
    return key_and_value[1].strip()

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        lines = get_metrics()
        server_threads =GaugeMetricFamily('http_server_threads', 'Help text',)
        for i in lines:
            if "ServerUptime" in i:
                v = split_pair(i)
                yield CounterMetricFamily('http_server_uptime', 'Help text', value=v)
            elif "BusyWorkers" in i:
                v = split_pair(i)
                server_threads.add_metric(['busy'], v)
            elif "IdleWorkers" in i:
                v = split_pair(i)
                server_threads.add_metric(['idle'], v)
        
        yield server_threads

REGISTRY.register(CustomCollector())