from urllib import request
import re

# === open proxy session in REQUEST ===
def useproxy(proxyserver):
    proxy = request.ProxyHandler(proxyserver)
    opener = request.build_opener(proxy)
    request.install_opener(opener)

# === Create list with available proxy ===
def getproxies():
    res_proxy = 'http://multiproxy.org/txt_all/proxy.txt'
    proxies = str(request.urlopen(res_proxy).read())
    servers = re.findall(r'\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}:\d{,}', proxies)
    proxylist = list(servers)
    return(proxylist)

# === Validate Proxy Server ===
def validate_proxy(proxy):
    useproxy(proxy)
    r = request.urlopen('https://httpbin.org/get')
    print(r.read())

def check_ip():
    r = str(request.urlopen('http://ifconfig.me/ip').read())
    ip = re.search(r'\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}', r)
    print(ip.group())

proxy = {'http': '66.57.1.142:9090'}
#validate_proxy(proxy)
#useproxy(proxy)
check_ip()


#g = getproxies()
#print(g)