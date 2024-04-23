import contextlib
from os import listdir, mkdir, remove
from random import choice, choices, randint, shuffle
from threading import Thread
from time import time

from bs4 import BeautifulSoup as bs
from colorama import Fore, init
from requests import get as G

tt = time()
init(True)
def Banner():
    banner = '''
                _______    _          _          _______    _______    _______    _______    _______   
    |\\     /|  (  ___  )  ( \\        ( \\        (  ____ )  (  ___  )  (  ____ )  (  ____ \\  (  ____ )  
    | )   ( |  | (   ) |  | (        | (        | (    )|  | (   ) |  | (    )|  | (    \\/  | (    )|  
    | | _ | |  | (___) |  | |        | |        | (____)|  | (___) |  | (____)|  | (__      | (____)|  
    | |( )| |  |  ___  |  | |        | |        |  _____)  |  ___  |  |  _____)  |  __)     |     __)  
    | || || |  | (   ) |  | |        | |        | (        | (   ) |  | (        | (        | (\\ (     
    | () () |  | )   ( |  | (____/\\  | (____/\\  | )        | )   ( |  | )        | (____/\\  | ) \\ \\__  
    (_______)  |/     \\|  (_______/  (_______/  |/         |/     \\|  |/         (_______/  |/   \\__/                                                                                                         
    '''
    print(Fore.LIGHTWHITE_EX+banner)
    print(f'{Fore.LIGHTWHITE_EX}      <<<<<<<<<<<<<>>>>>>>>>>>>>')
    print(f"{Fore.LIGHTBLUE_EX}        Version : 3.5.6")
    print(f"{Fore.LIGHTRED_EX}        Developer: Ayush Kumar")
    print(f'{Fore.LIGHTWHITE_EX}      <<<<<<<<<<<<<>>>>>>>>>>>>>')

with contextlib.suppress(Exception):
    mkdir('./Py_wallpaper')
    print('Setting up things for the first time!!!')
tmp_link, final_links, threads, old_wp, category = [], [], [], listdir('./Py_wallpaper'), ['abstract','technology','minimalism','futuristic','digital','art','pattern','illustration','creativity','illuminated','artwork','space','sky','architecture']
def wp_flare():
    cho_ice = str(choice(category))
    category.remove(cho_ice)
    wp = G(''.join(['https://www.wallpaperflare.com/search?wallpaper=',cho_ice,'&page=',str(randint(1,80))]),timeout=5).content
    soup = bs(wp,'lxml')
    lnk = soup.find_all('a',attrs={'itemprop':'url'})
    for i in lnk:
        tmp_link.append(''.join([i['href'],'/download']))

def wp_flare_download(dl_links):
    fetch = G(dl_links,timeout=10).content
    soup = bs(fetch,'lxml')
    with contextlib.suppress(Exception):
        dl_lnk = soup.find('img',attrs={'itemprop':"contentUrl"})['src'] # type: ignore
        final_links.append(dl_lnk)
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

def thrd(lnk):
    r = G(lnk, stream=True,timeout=10).content
    with open(''.join(['./Py_wallpaper/',lnk.split("/")[-1]]), 'wb') as f:
        f.write(r)

for link in final_links:
    t = Thread(target=thrd, args=(link,))
    t.start()
    threads.append(t)

for old_wlp in old_wp:
    remove(f'./Py_wallpaper/{str(old_wlp)}')

for thread in threads:
    thread.join()

print(time()-tt)