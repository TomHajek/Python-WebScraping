import requests
import pandas
from bs4 import BeautifulSoup as bs

r = requests.get("https://www.century21.cz/nemovitosti?search%5Bttype%5D%5B0%5D=sale&search%5Bptype%5D=flat&search%5Boptions%5D%5Bflat%5D%5Bdisposition%5D%5B0%5D=2%2B1&search%5Boptions%5D%5Bflat%5D%5Bdisposition%5D%5B1%5D=2%2Bkk&search%5Boptions%5D%5Bflat%5D%5Bdisposition%5D%5B2%5D=3%2B1&search%5Boptions%5D%5Bflat%5D%5Bdisposition%5D%5B3%5D=3%2Bkk&search%5Bprice_to%5D=7500000&search%5Blocality%5D%5B0%5D=1")
c = r.content


soup = bs(c, "html.parser")
all = soup.find_all("div", {"class": "advertise media item"})


for item in all:
    try:
        print(item.find("span", {"class", "amount"}).text)
        print(item.find("div", {"class", "media-body"}).find("p").text) 
        print(item.find("div", {"class", "media-body"}).find("h4").find("a").text)
    except:
        print(None)
    
    print(" ")


l = []
for item in all:
    d = {}

    try:
        d["Cena"] = item.find("span", {"class", "amount"}).text
    except:
        d["Cena"] = None
    
    try:
        d["Adresa"] = item.find("div", {"class", "media-body"}).find("p").text          
    except:
        d["Adresa"] = None  
        
    try:
        d["Popis inzerátu"] = (item.find("div", {"class", "media-body"}).find("h4").find("a").text)
    except:
        d["Popis inzerátu"] = None
    
    l.append(d)


df = pandas.DataFrame(l)
df.to_csv("inzeraty.csv")