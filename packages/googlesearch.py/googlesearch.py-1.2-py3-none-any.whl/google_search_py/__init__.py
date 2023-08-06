"""
MIT License

Copyright (c) 2021 Sijey

Read more : https://raw.githubusercontent.com/sijey-praveen/YouTube-Music-API/Sijey/LICENSE

"""

from requests import get, head
from bs4 import BeautifulSoup
import socket
import platform
from os import system

def NoInternetError():
    if "127.0.0.1" == socket.gethostbyname(socket.gethostname()):
        print("You're Offline, Please Connect To Internet!")

def check_for_update():
    if 200 == head("https://pypi.org/project/googlesearch.py/1.3/").status_code:
        if "Windows" == platform.system():
            system("pip install googlesearch.py==1.3")
        elif "Darwin" == platform.system():
            system("pip install googlesearch.py==1.3")
        elif "Linux" == platform.system():
            system("pip install googlesearch.py==1.3")

def site_url(query, lang="en", num=1):
    try:
        usr_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/61.0.3163.100 Safari/537.36'}
        result_block = BeautifulSoup(get(f'https://www.google.com/search?q={query}&num={num}&hl={lang}', headers=usr_agent).text, 'html.parser').find_all('div', attrs={'class': 'g'})
        for result in result_block:
            return result.find('a', href=True)['href']
    except Exception:
        return "Something went wrong!"

def site_title(url):
    try:
        for tag in BeautifulSoup(get(url).text, 'html.parser').find_all("meta"):
            if tag.get("property", None) == "og:title":
                return str(tag.get("content", None))
    except Exception:
        return "Something went wrong!"

def site_description(url):
    try:
        for tag in BeautifulSoup(get(url).text, 'html.parser').find_all("meta"):
            if tag.get("property", None) == "og:description":
                return str(tag.get("content", None))
    except Exception:
        return "Something went wrong!"

def site_favicon(url):
    try:
        return f"https://www.google.com/s2/favicons?domain={url}"
    except Exception:
        return "Something went wrong!"

def search(query):
    url = site_url(query=query)
    return dict(title = site_title(url), description = site_description(url), url = url, favicon = site_favicon(url))

if __name__ == "__main__":
    NoInternetError()
    check_for_update()