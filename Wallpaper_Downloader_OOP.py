from contextlib import suppress
from os import listdir, mkdir, remove
from random import choice, randint
from threading import Thread
from time import time
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs
from colorama import Fore, init
from requests import get as G
from sys import exit

init(True)

with suppress(Exception):
    mkdir('./Py_wallpaper')
    print('Setting up things for the first time!!!')

class WallpaperDownloader:
    def __init__(self, category: str):
        self.__startTime = time()
        self.category = category.replace(" ","+")
        self.__urlContent = self.__getCorrectUrlContent()
        self.__oldWallpaper = set(listdir('./Py_wallpaper'))
        self.__threads = []
        self.__finalWallpaperLink = set()

    def __getCorrectUrlContent(self):
        urlContent = G(url = f'https://www.wallpaperflare.com/search?wallpaper={self.category}&page={randint(1,80)}',timeout=10).content
        if len(urlContent) <= 1582:
            return G(url = f'https://www.wallpaperflare.com/search?wallpaper={self.category}',timeout=10).content
        return urlContent
    
    def __extractUrl(self):
        soup = bs(self.__urlContent,'lxml')
        links = soup.find_all('a',attrs={'itemprop':'url'})
        for link in links:
            yield (''.join([link['href'],'/download']))

    def __parseMainUrl(self, urlContent):
        fetch = G(urlContent,timeout=10).content
        soup = bs(fetch,'lxml')
        with suppress(Exception):
            dl_lnk = soup.find('img',attrs={'itemprop':"contentUrl"})['src'] # type: ignore
            self.__finalWallpaperLink.add(dl_lnk)

    def __downloaderUtil(self, url):
        r = G(url, stream=True,timeout=10).content
        with open(''.join(['./Py_wallpaper/',url.split("/")[-1]]), 'wb') as f:
            f.write(r)
            f.close()

    def __fetchMainUrl(self):
        for mainUrl in self.__extractUrl():
            thread = Thread(target=self.__parseMainUrl, args=(mainUrl,))
            thread.start()
            self.__threads.append(thread)
        print(f"{Fore.LIGHTMAGENTA_EX}Downloading {self.category.capitalize()} Wallpapers\nPlease Wait...")
        for thrd in self.__threads:
            thrd.join()
    
    def __cleanupActivity(self):
        for old_wlp in self.__oldWallpaper:
            with suppress(Exception):
                remove(f'./Py_wallpaper/{old_wlp}')

    def downloadWallpapers(self):
        self.__fetchMainUrl()
        with ThreadPoolExecutor(max_workers=20) as Executer:
            for link in self.__finalWallpaperLink:
                Executer.submit(self.__downloaderUtil, link)
        print(f"{Fore.LIGHTGREEN_EX}Wallpapers Downloaded in {round(time()-self.__startTime,2)} Seconds")
        print("================================")
        print(f"{Fore.LIGHTYELLOW_EX}Performing Cleanup...")
        self.__cleanupActivity()
        print("================================")
        print(f"{Fore.LIGHTRED_EX}Exiting...")
        exit()
        

def displayBanner():
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
    print(f"{Fore.LIGHTBLUE_EX}        Version : 3.8.2")
    print(f"{Fore.LIGHTRED_EX}        Developer: Ayush Kumar")
    print(f'{Fore.LIGHTWHITE_EX}      <<<<<<<<<<<<<>>>>>>>>>>>>>')

if __name__ == '__main__':
    displayBanner()
    categories = ['abstract','technology','futuristic','digital','creativity','space','black','oled','dark','night', 'cars','sports+cars']
    print(f"\n{Fore.LIGHTWHITE_EX}User Choices:")
    print(f"{Fore.LIGHTWHITE_EX}'Y' -> (yes)\n'N' -> (no)\n'C' -> (Custom Category)\n'E' -> Exit\n")
    while 1:
        cho_ice = str(choice(categories)).capitalize()
        print(f"{Fore.LIGHTWHITE_EX}Download {cho_ice} Wallpapers?")
        inp = input(f"{Fore.LIGHTWHITE_EX}Enter Your Choice -> ")
        if inp in {"y","Y"}:
            wallpaperDownloader = WallpaperDownloader(category = cho_ice)
            wallpaperDownloader.downloadWallpapers()
        elif inp in {'C','c'}:
            category = str(input(f"{Fore.LIGHTWHITE_EX}Enter Your Own Category:-> "))
            wallpaperDownloader = WallpaperDownloader(category=category)
            wallpaperDownloader.downloadWallpapers()
        elif inp in {'e',"E"}:
            break
        elif inp in {"n","N"}:
            categories.remove(cho_ice)
        else:
            print(f"{Fore.LIGHTRED_EX}Invalid Input! Try Again!")
    exit()