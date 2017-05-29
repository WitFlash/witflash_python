from urllib import request
import http.client
import sys, os

# Get current client's IP in Web and print on the screen
def current_ip():
    connection = http.client.HTTPConnection('ifconfig.me')
    connection.request('GET', '/ip')
    response = connection.getresponse().read()
    print('Current IP: %s' % response)
# ======================================================

# === open proxy session in REQUEST ===
def useproxy():
    proxies = {'http': '83.142.110.69:8081',
    'http': '109.254.6.40:8080',
    'http': '212.114.99.36:80',
    'http': '36.66.253.17:8088'
    }
    print(type(proxies))
    proxy = request.ProxyHandler(proxies)
    opener = request.build_opener(proxy)
    request.install_opener(opener)
# =====================================

useproxy()
r = request.urlopen('http://ifconfig.me/ip').read()
print(r)


