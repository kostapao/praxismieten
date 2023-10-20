import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import numpy as np


def get_doc_info(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_doc_page = urlopen(req).read()
    soup = BeautifulSoup(html_doc_page, 'html.parser')
    # Find all <td> elements with class "outer-firmen-name" and "outer-more-1"
    outer_firmen_name_elements = soup.find_all('td', class_='outer-firmen-name')
    outer_more_1_elements = soup.find_all('td', class_='outer-more-1')
    doc_info = ""
    # Extract and print the content from each <td> element
    for element in outer_firmen_name_elements + outer_more_1_elements:
        content = element.get_text(strip=True)
        doc_info += "_" + content
    return doc_info


#Get all zg doc links

req = Request('https://www.doktor.ch/aerzte/aerzte_k_zg.html', headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()
soup = BeautifulSoup(html_page, 'html.parser')

href_list = []

for fachbezeichnung in soup.find_all(class_="novip-firmen-name"):
    href_list.append(fachbezeichnung["href"])

for fachbezeichnung in soup.find_all(class_="vip-firmen-name"):
    href_list.append(fachbezeichnung["href"])

concatinated_links = []

concat_link = "https://www.doktor.ch"
for href in href_list:
    concatinated_links.append(concat_link+href)

lu_list = []

for link in concatinated_links:
    try:
        content = get_doc_info(link)
        lu_list.append(content)
    except:
        print(link)


lu_df = pd.DataFrame()

lu_df["doc_info"] = lu_list


lu_df.to_pickle("zg_docs")


lu_df.to_excel("zg_docs.xlsx")



