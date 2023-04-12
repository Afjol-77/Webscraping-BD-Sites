import requests
import time
from threading import Thread
import os
import lxml
import pandas as pd
from bs4 import BeautifulSoup
import json


HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
	            'Accept-Language': 'en-US, en;q=0.5'})

print("Search Tag: ")
tag = input()
tag = tag.replace(" ","+")
result = []
sorted_result =[]



#Evaly Scraping
def evaly():
  site_url = "https://evaly.com.bd/search?page=1&term="+tag
  webpage = requests.get(site_url, headers=HEADERS)
  web = webpage.text
  soup = BeautifulSoup(web, "lxml")
  box = soup.find("div", class_="flex gap-4")

  names = box.find_all("p", class_ ="font-medium text-base line-clamp-2 hover:underline h-[47px]")
  prices = box.find_all("p",class_ ="text-sm font-medium text-gray-800 md:text-lg")
  images = box.find_all("img")
  urls = box.find_all("a")

  for i in range(0,5):
    name = names[i].text
    price = int(prices[i].text[1:])
    image = images[i].get("src")
    url = urls[i].get("href")
    f_url = "https://evaly.com.bd"+url
    site = "Evaly"
    object = {}
    object["Name"] = name
    object["Price"] = price
    object["img"] = image
    object["URL"] = f_url
    object["Site"] = site
    result.append(object)

#Gadgetandgear Scraping
def gadgetandgear():
  site_url = "https://gadgetandgear.com/search?keyword="+tag
  webpage = requests.get(site_url, headers=HEADERS)
  web = webpage.text
  soup = BeautifulSoup(web, "lxml")
  box = soup.find("div", class_="col-12 mt-3 px-lg-0")

  names = box.find_all("p", class_ ="product-name d-block mb-0")
  prices = box.find_all("p",class_ ="product-price text-bold mb-0")
  images = box.find_all("img")
  
  urls = box.find_all("a")

  for i in range(0,5):
    name = names[i].text
    price = prices[i].text.strip()
    price = price.translate({ord('\n'): None})
    pos = 0
    cnt = 0
    for j in range(0, len(price)-1):
      if price[j] == 'T':
        cnt += 1
      if cnt == 2:
        pos=j
        break
    if cnt == 2:
      price = price[:pos]
    price = price.translate({ord(','): None})
    price = price[4:]
    price = int(float(price))
    image = images[i].get("data-src")
    url = urls[i].get("href")
    site = "GadgetandGear"
    object = {}
    object["Name"] = name
    object["Price"] = price
    object["img"] = image
    object["URL"] = url
    object["Site"] = site
    result.append(object)

#BD Shop Scraping
def bdshop():
  site_url = "https://www.bdshop.com/catalogsearch/result/?q="+tag
  webpage = requests.get(site_url, headers=HEADERS)
  web = webpage.text
  soup = BeautifulSoup(web, "lxml")

  names = soup.find_all("h2", class_ ="product name product-item-name")
  prices = soup.find_all("span", {"data-price-type": "finalPrice"})
  images = soup.find_all("span", class_="main-photo")
  urls = soup.find_all("a", class_="product-item-link")

  for i in range(0,5):
    name = names[i].text.replace("&nbsp;", " ")
    price = prices[i].text[1:]
    price = price.translate({ord(','): None})
    price = int(float(price))

    image = images[i].find("img", class_="product-image-photo").get("src")
    url = urls[i].get("href")
    site = "BD Shop"
    object = {}
    object["Name"] = name
    object["Price"] = price
    object["img"] = image
    object["URL"] = url
    object["Site"] = site

    result.append(object)

#Calling Functions
evaly()
gadgetandgear()
bdshop()

print("Sort Price by [ASC/DESC]?")
sort_by = input()
sort_by = sort_by.lower()
if sort_by == "asc":
  sorted_result = sorted(result, key=lambda d: d['Price'])
elif sort_by == "desc":
  sorted_result = sorted(result, key=lambda d: d['Price'], reverse=True)

for i in sorted_result:
  i['Price'] = "Tk "+str(i['Price'])

final = json.dumps(sorted_result, indent=2)
print(final)
with open("webscraping_bd.json", "w") as outfile:
   outfile.write(final)

