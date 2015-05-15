#!/usr/bin/env python

""" Download comics from commitstrip.com
Heavily inspired by http://automatetheboringstuff.com/chapter11/
"""

import requests
import bs4
import os
import time

if __name__ == '__main__':

    url = 'http://www.commitstrip.com/fr/'
    os.makedirs('commitstrip', exist_ok=True)
    while not url.endswith('#'):
        print('Downloading page %s...' % url)
        try:
            res = requests.get(url)
            # for politeness
            time.sleep(1)

            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text)

            # Find the URL of the comic image in the div of class entry-content
            comicElem = soup.find("div", class_="entry-content").find("img")
            if comicElem == []:
                print('Could not find comic image.')
            else:
                comicUrl = comicElem.get('src')
                print('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl)
                res.raise_for_status()

                # Save the image to ./commitstrip folder
                imageFile = open(os.path.join('commitstrip', os.path.basename(comicUrl)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()

            # Get the Next button's url <a class="nextpostslink" href="http://www.commitstrip.com/en/page/2/">»</a>
            prevLink = soup.select('a[class="nextpostslink"]')[0]
            url = prevLink.get('href')

        except requests.exceptions.HTTPError:
            continue

    print('Done.')