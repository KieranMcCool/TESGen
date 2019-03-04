#!/usr/bin/env python3

# Author: Kieran McCool
# Description: This script scrapes http://uesp.net (the unofficial elder scrolls pages wiki)
#              for all names in the Elder Scrolls universe (so far) by race and gender.
#              It outputs files for each into the ./DataSets directory.

import os.path
from re import sub
import requests
from bs4 import BeautifulSoup, Tag

races = ['Altmer', 'Argonian', 'Bosmer', 'Breton', 'Dunmer',
            'Imperial', 'Khajiit', 'Nord', 'Orc', 'Redguard']

url = 'https://en.uesp.net/wiki/Lore:%s_Names'
base_file_name = './DataFiles/%s_%s_names.txt'

def getPage(race):
    html = requests.get(url % (race)).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getNames(soup, race):
    headers = soup.findAll('h3')
    maleNameHeaders = headers[1:10]
    femaleNameHeaders = headers[11:19]

    # TODO: family names need a different parsing method.
    # familyNameHeaders = headers[20:27]

    for i, gender in enumerate([maleNameHeaders, femaleNameHeaders]):
        with open(base_file_name % ( ['Male', 'Female'][i], race), 'w') as output:
            for game in gender:
                raw_text = game.findNextSibling('p').text.replace('\n', ', ')
                stripped_text = sub(r'\([\d, .]*\)', '', raw_text)
                stripped_text = sub(r'^(.)*:', '', stripped_text)
                stripped_text = '\n'.join(set([s.strip() 
                    for s in stripped_text.split(',') if s.strip() != '']))
                output.write(stripped_text + '\n')

def main():

    if not os.path.exists('./DataFiles'):
        os.mkdir('./DataFiles')

    for race in races:
        soup = getPage(race)
        getNames(soup, race)

if __name__ == "__main__":
    main()
