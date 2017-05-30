from urllib import request
from random import choice
import re

# === open proxy session in REQUEST ===
def start(proxyserver):
    proxy = request.ProxyHandler(proxyserver)
    opener = request.build_opener(proxy)
    request.install_opener(opener)

# === open proxy session with random proxy from list ===
def random(proxylist):
    if proxylist:
        random_proxy = choice(proxylist)
        print('Will use %s proxy server' % random_proxy)
        proxyserver = {'http': random_proxy}
        start(proxyserver)

# === Create list with available proxy ===
def getlist():
    res_proxy = 'http://www.proxylists.net'
    proxies = str(request.urlopen(res_proxy).read())
    servers = re.findall(r'\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}:\d{1,5}', proxies)
    proxylist = list(servers)
    if proxylist == []:
        return(False)
    valide_proxy = validate(proxylist)
    if valide_proxy == []:
        return(False)
    return(valide_proxy)

# === Validate Proxy Server ===
def validate(proxylist, valide_proxy=[]):
    for proxyserver in proxylist:
        start({'http': proxyserver})
        try:
            r = request.urlopen('https://httpbin.org/get')
            print('%s added to proxy list' % proxyserver)
            valide_proxy.append(proxyserver)
        except:
            print('%s NOT VALIDATE' % proxyserver)
            continue
    print('\n')
    return(valide_proxy)

# === Check current IP adress ===
def check_ip():
    r = str(request.urlopen('http://ifconfig.me/ip').read())
    ip = re.search(r'\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}', r)
    print(ip.group())

# TEMPLATES FOR USE MODULES: 
# proxylist = getlist()
# random(proxylist)
# check_ip()