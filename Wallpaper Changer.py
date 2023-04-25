from os import listdir, remove, mkdir
from random import randint, choices, shuffle, choice
from colorama import Fore, init
from requests import get as G
from threading import Thread
from bs4 import BeautifulSoup as bs
from time import time, sleep
tt = time()
init(True)
def Banner():
    banner = '''
                _______    _          _          _______    _______    _______    _______    _______   
    |\     /|  (  ___  )  ( \        ( \        (  ____ )  (  ___  )  (  ____ )  (  ____ \  (  ____ )  
    | )   ( |  | (   ) |  | (        | (        | (    )|  | (   ) |  | (    )|  | (    \/  | (    )|  
    | | _ | |  | (___) |  | |        | |        | (____)|  | (___) |  | (____)|  | (__      | (____)|  
    | |( )| |  |  ___  |  | |        | |        |  _____)  |  ___  |  |  _____)  |  __)     |     __)  
    | || || |  | (   ) |  | |        | |        | (        | (   ) |  | (        | (        | (\ (     
    | () () |  | )   ( |  | (____/\  | (____/\  | )        | )   ( |  | )        | (____/\  | ) \ \__  
    (_______)  |/     \|  (_______/  (_______/  |/         |/     \|  |/         (_______/  |/   \__/                                                                                                         
    '''
    ver = "        Version : 3.4.6"
    cre = "        Developer: Ayush Kumar"
    print(Fore.LIGHTWHITE_EX+banner)
    print(Fore.LIGHTWHITE_EX+'      <<<<<<<<<<<<<>>>>>>>>>>>>>')                   
    print(Fore.LIGHTBLUE_EX+ ver)
    print(Fore.LIGHTRED_EX+ cre)
    print(Fore.LIGHTWHITE_EX+'      <<<<<<<<<<<<<>>>>>>>>>>>>>')

try:
    mkdir('./Py_wallpaper')
    print('Setting up things for the first time!!!')
except:
    pass
tmp_link, final_links, threads, old_wp, category = [], [], [], listdir('./Py_wallpaper'), ['abstract','technology','minimalism','futuristic','digital','art','pattern','illustration','creativity','illuminated','artwork','space','sky','architecture']
def wp_flare():
    cho_ice = str(choice(category))
    category.remove(cho_ice)
    wp = G(''.join(['https://www.wallpaperflare.com/search?wallpaper=',cho_ice,'&page=',str(randint(1,80))]),timeout=5).content
    soup = bs(wp,'lxml')
    lnk = soup.find_all('a',attrs={'itemprop':'url'})
    for l in lnk:
        # if "anime" not in l['href']:
            tmp_link.append(''.join([l['href'],'/download']))

def wp_flare_download(dl_links):
    fetch = G(dl_links).content
    soup = bs(fetch,'lxml')
    try:
        dl_lnk = soup.find('img',attrs={'itemprop':"contentUrl"})['src']
        final_links.append(dl_lnk)
    except:
        pass
Banner()
wp_flare()
# wp_flare()
print("Downloading cool Wallpapers")
shuffle(tmp_link)
tmp_link= choices(tmp_link,k=50)
for l in tmp_link:
    a = Thread(target=wp_flare_download,args=(l,))
    a.start()
    threads.append(a)
for thread in threads:
    thread.join()

def thrd(link):
    r = G(link, stream=True).content
    with open(''.join(['./Py_wallpaper/',link.split("/")[-1]]), 'wb') as f:
        f.write(r)

for link in final_links:
    t = Thread(target=thrd, args=(link,))
    t.start()
    threads.append(t)
for thread in threads:
    thread.join()

for old_wlp in old_wp:
   remove('./Py_wallpaper/'+str(old_wlp))
print(time()-tt)
sleep(2)
