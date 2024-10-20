import requests
from geoip import geolite2

CONNECTIONS = []

def refresh_proxies_from_url(proxy_list_url):
    try:
        response = requests.get(proxy_list_url)
        proxies = response.text.split('\n')
        CONNECTIONS.extend([{"address": proxy, "type": "http"} for proxy in proxies if validate_proxy('http', proxy)])
    except Exception as e:
        print(f"[ERROR] Could not refresh proxies: {e}")

def match_proxies_to_region(ip_address):
    location = geolite2.lookup(ip_address)
    region = location.country if location else 'default'
    return [proxy for proxy in CONNECTIONS if proxy['region'] == region]