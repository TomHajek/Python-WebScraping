import requests
import pandas
from bs4 import BeautifulSoup as bs

# Storing page into a variable
base_url = "https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/praha/2-1,3-kk,3-1?_token=K8yMdjiiTunwv91ImVHdzuXY0WR_yifmcE8nNUCxYGQ&order=price_asc"

# Getting cached URL page content
r = requests.get(base_url + ".html")

# Read content
c = r.content

# Parse html data(content)
soup = bs(c, "html.parser")

# Divide data to each advertisement box
all = soup.find_all("div", {"class": "mb-4"})

# Lets take a look how many pages were found
# NOTE: pagination router have the first button as "Previous" and last one as "Next", so take it into an account
# To be able to find the last page, I had to loop for penultimate (předposlední) element:
page_nr = soup.find_all("a", {"class": "page-link pagination__page"})[-2].text
print(f"We found {page_nr} pages.")

# Create an empty list
l = []

"""
Im not sure, if I will be able to loop through all pages at once, since the first page has different URL.
So I will probably loop first page separately and then use loop for pages 2-18.
"""

# Looping the first page alone
for item in all:

    # Create an empty dictionary
    d = {}

    # Store scraped elements into a dictionary, to be able to frame data
    try:
        d["Adresa"] = item.find("h3", {"class", "product__title font-size-15 mb-0"}).find("a", {"class",
                                                                                                "product__link js-product-link"}).text.replace(
            "\n", "")
    except:
        d["Adresa"] = None

    try:
        d["Popis"] = item.find("p", {"class", "product__note"}).text.strip()
    except:
        d["Popis"] = None

    try:
        d["Cena"] = item.find("span", {"class", "items items--lg"}).find("span", {"class", "items__item"}).find(
            "strong", {"class", "product__value"}).text.replace(" ", "").replace("Kč", "").replace("\n", "")
    except:
        d["Cena"] = None

        # Additional informations with no unique tag
    for column_tags in item.find_all("div", {"class": "tag"}):

        if "Balkón" in column_tags.text:
            d["Balkón"] = "Ano"  # column_tags.text.replace("\n", "")
        else:
            d["Balkón"] = "Ne"

        if "Lodžie" in column_tags.text:
            d["Lodžie"] = "Ano"  # column_tags.text.replace("\n", "")
        else:
            d["Lodžie"] = "Ne"

        if "Výtah" in column_tags.text:
            d["Výtah"] = "Ano"  # column_tags.text.replace("\n", "")
        else:
            d["Výtah"] = "Ne"

        if "Sklep" in column_tags.text:
            d["Sklep"] = "Ano"  # column_tags.text.replace("\n", "")
        else:
            d["Sklep"] = "Ne"

        if "Garáž" in column_tags.text:
            d["Garáž"] = "Ano"  # column_tags.text.replace("\n", "")
        else:
            d["Garáž"] = "Ne"

        if "Parkování" in column_tags.text:
            d["Parkování"] = "Ano"  # column_tags.text.replace("\n", "")
        else:
            d["Parkování"] = "Ne"

    # Storing dictionaries (of each advertisement) into the list
    l.append(d)

# Crawling through the webpages (pages 2-18)
for page in range(0, int(page_nr)):
    print()

    # Getting data from cached URL
    # https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/praha/2-1,3-kk,3-1?_token=K8yMdjiiTunwv91ImVHdzuXY0WR_yifmcE8nNUCxYGQ&order=price_asc
    # https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/praha/2-1,3-kk,3-1?_token=K8yMdjiiTunwv91ImVHdzuXY0WR_yifmcE8nNUCxYGQ&order=price_asc&page=2
    # https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/praha/2-1,3-kk,3-1?_token=K8yMdjiiTunwv91ImVHdzuXY0WR_yifmcE8nNUCxYGQ&order=price_asc&page=18
    r = requests.get(base_url + "&page=" + str(page) + ".html")
    c = r.content
    # c=r.json()["list"]

    # Parsing data
    soup = bs(c, "html.parser")
    all = soup.find_all("div", {"class": "mb-4"})

    # Looping through the scraped data of pages 2-18
    for item in all:
        # Create an empty dictionary
        d = {}

        # Store scraped elements into a dictionary, to be able to frame data
        try:
            d["Adresa"] = item.find("h3", {"class", "product__title font-size-15 mb-0"}).find("a", {"class",
                                                                                                    "product__link js-product-link"}).text.replace(
                "\n", "")
        except:
            d["Adresa"] = None

        try:
            d["Popis"] = item.find("p", {"class", "product__note"}).text.strip()
        except:
            d["Popis"] = None

        try:
            d["Cena"] = item.find("span", {"class", "items items--lg"}).find("span", {"class", "items__item"}).find(
                "strong", {"class", "product__value"}).text.replace(" ", "").replace("Kč", "").replace("\n", "")
        except:
            d["Cena"] = None

            # Additional informations with no unique tag
        for column_tags in item.find_all("div", {"class": "tag"}):

            if "Balkón" in column_tags.text:
                d["Balkón"] = "Ano"  # column_tags.text.replace("\n", "")
            else:
                d["Balkón"] = "Ne"

            if "Lodžie" in column_tags.text:
                d["Lodžie"] = "Ano"  # column_tags.text.replace("\n", "")
            else:
                d["Lodžie"] = "Ne"

            if "Výtah" in column_tags.text:
                d["Výtah"] = "Ano"  # column_tags.text.replace("\n", "")
            else:
                d["Výtah"] = "Ne"

            if "Sklep" in column_tags.text:
                d["Sklep"] = "Ano"  # column_tags.text.replace("\n", "")
            else:
                d["Sklep"] = "Ne"

            if "Garáž" in column_tags.text:
                d["Garáž"] = "Ano"  # column_tags.text.replace("\n", "")
            else:
                d["Garáž"] = "Ne"

            if "Parkování" in column_tags.text:
                d["Parkování"] = "Ano"  # column_tags.text.replace("\n", "")
            else:
                d["Parkování"] = "Ne"

        # Storing dictionaries (of each advertisement) into the list
        l.append(d)

# Transforming data into the tab, using pandas library
df = pandas.DataFrame(l)
#df

# Exporting tab into CSV file
df.to_csv("bezrealitky.csv")