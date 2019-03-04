#!/usr/bin/env python3

# Author: Kieran McCool
# Description: This script scrapes http://uesp.net (the unofficial elder scrolls pages wiki)
#              for all names in the Elder Scrolls universe (so far) by race and gender.
#              It outputs files for each into the ./DataSets directory.

import requests
from re import sub
from bs4 import BeautifulSoup, Tag

url = 'https://en.uesp.net/wiki/Lore:%s_Names'
base_file_name = '%s_%s_names.txt'

def getPage():
    race = 'Altmer'
    html = requests.get(url % (race)).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getNames(soup, baseFileName):
    headers = soup.findAll('h3')
    maleNameHeaders = headers[1:10]
    femaleNameHeaders = headers[11:19]
    # familyNameHeaders = headers[20:27]

    for gender in [maleNameHeaders, femaleNameHeaders]:
        for game in gender:
            raw_text = game.findNextSibling('p').text
            stripped_text = sub(r'\([\d, .]*\)', '', raw_text)
            stripped_text = sub(r'(\d)*x:', '', stripped_text)
            stripped_text = '\n'.join(set([s.strip() for s in stripped_text.split(',')]))
            print(stripped_text)

def main():
    soup = getPage()
    getNames(soup, )

if __name__ == "__main__":
    main()
