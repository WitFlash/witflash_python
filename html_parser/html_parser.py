from urllib import request
from html.parser import HTMLParser
import sys, os

class myHTMLParser(HTMLParser): # class for parse main page
    def __init__(self, protocol, site_name, url, *args, **kwargs):
        self.find_links = [] # list for links that find on the page
        self.protocol = protocol
        self.site_name = site_name
        self.url = url # link with 'http(s)://'
        super().__init__(*args, **kwargs)
        print('Checking %s ...' % self.url)
        try:
            self.feed(self.read_site_content())
            self.create_file() # in this file will be keep all urls from site
            self.add_url() # adding url to Map Site file (necessary links only)
        except TypeError:
            print("Error on the page.")
        with open('checked_links.txt', 'a') as f:
            f.write(self.url + '\n') # add url in checked list
        print('The page has been checked.\n')
    def handle_starttag(self, tag, attrs): # find correct url on the page
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    link = self.validate(attr[1]) # validate link. will be only 'html' format
                    if link != '' and link not in self.find_links:
                        self.find_links.append(link) # add to list
    def validate(self, link): 
        if len(link) == 0: # if find empty url
            return('')
        elif link in self.find_links or '#' in link or '?' in link or 'javascript:' in link or link == '/' or '.php' in link: # if link go to the start page or it's script
            return('')
        elif link[0] != '/' and self.site_name not in link:
            return('')
        else:
            return(self.check_link(link))
    def check_link(self, link):
        if link[0] == '/':
            link_to_check = self.protocol + self.site_name + link.rstrip('/')
        else:
            link_to_check = link.rstrip('/')
        return(link_to_check)
    def read_site_content(self):
        try:
            url = request.urlopen(self.url).read()
            return(str(url))
        except:
            print("URL %s not available." % self.url)    
    def create_file(self):
        try:
            with open('urls.txt', 'r') as f: 
                urls = f.read().split('\n')
        except:
            urls = []
        with open('urls.txt', 'a') as f:
            count = 0
            for url in self.find_links:
                if url not in urls:
                    f.write(url + '\n')
                    count += 1
            if count != 0:
                print('%s links added from %s' % (count, self.url))
    def add_url(self):
        with open('map_site.txt', 'a') as write_ms:
            write_ms.write(self.url + '\n')
            print('%s added to Map Site.' % self.url)
def check_protocol(site):
    protocol = ['https://', 'http://']
    for i in protocol:
        url = i + site
        try:
            response = request.urlopen(url)
            print('%s is correct \n' % url)
            return(i)
        except:
            print('%s is not available' % url)
            continue
    print("Site is not available on https or http protocol.\nPlease make another choise.\n")
    return(False)
def start():
    while True:
        site = input('Enter site name that you want to parse (without "http://" or "https://") or type \"E\" to Exit:\n')
        if site == 'E':
            sys.exit()
        response = check_protocol(site)
        if response == False: 
            continue
        else: 
            return([response, site])
def resume(dir_site):
    print('You already try to check this site. Do you want to resume this project or start over?')
    while True:
        usr_choice = input('(R)esume / (S)tart from begin: ')
        if usr_choice == 'R':
            break
        elif usr_choice == 'S':
            for file in os.listdir(dir_site):
                os.remove(file)
            break
        else:
            print('Please make the choice!')
def change_dir(site):
    dir_site = os.getcwd() + '\\' + site
    try:
        os.mkdir(dir_site)
        os.chdir(dir_site)
    except OSError:
        os.chdir(dir_site)
        resume(dir_site)
    with open('urls.txt', 'a') as f:
        f.write(full_site[0] + site + '\n')
    with open('checked_links.txt', 'a') as f:
        pass
def make_levels():
    with open('map_site.txt', 'r') as f:
        map_site = f.read().split('\n')
    for url in map_site:
        if 4 > url.count('/') >= 2:
            with open('level_1.txt', 'a') as level_1:
                level_1.write(url + '\n')
        elif url.count('/') == 4:
            with open('level_2.txt', 'a') as level_2:
                level_2.write(url + '\n')
        elif url.count('/') == 5:
            with open('level_3.txt', 'a') as level_3:
                level_3.write(url + '\n')

full_site = start()
protocol = full_site[0]
site = full_site[1]
change_dir(site) # change directory to the name of parsing site and create files "map_site" and "checked_list"
success = True # variable to stop parsing process if no link has been added to map_site (all links created already)

while success:
    success = False
    with open('urls.txt', 'r') as f:
        urls = f.read().split('\n')
    for url in urls:
        with open('checked_links.txt', 'r') as f:
            checked_links = f.read().split('\n')
        if url not in checked_links and url.count('/') < 6:
            parser = myHTMLParser(protocol, site, url)
            success = True

make_levels()
input('Job is done.\nPress any key to Exit.')