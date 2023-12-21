from bs4 import BeautifulSoup
import requests
import re
from typing import Dict, Set

#define function that sees if a word is inside a paragraph
def paragraph_mentions(text:str, key:str):
    soup = BeautifulSoup(text, 'html5lib')
    paragraphs = [p.get_text() for p in soup('p')]
    return any(key.lower() in paragraph.lower() for paragraph in paragraphs)

press_releases: Dict[str, Set[str]] = {}


#create regex for matching urls
regex = r"^https://.*\.house\.gov/?$"
senate_regex = r"^https://.*\.senate\.gov/?$"
url = ('https://www.house.gov/representatives')
senator_url = 'https://www.senate.gov/senators'

#House of Representatives
text = requests.get(url).text
soup = BeautifulSoup(text, 'html5lib')
all_urls = [a['href'] for a in soup('a') if a.has_attr('href')]
good_urls = [url for url in all_urls if re.match(regex, url)]
good_urls = set(good_urls)

#Senate
senate_Text = requests.get(senator_url).text
geriatricSoup = BeautifulSoup(senate_Text, 'html5lib')
senate_urls = [a['href'] for a in geriatricSoup('a') if a.has_attr('href')]
good_senate_urls = [url for url in senate_urls if re.match(senate_regex, url)]
good_senate_urls = set(good_senate_urls)

#Get all press-release urls for each representative
for house_url in good_urls:
    html = requests.get(house_url).text
    houseSoup = BeautifulSoup(html, 'html5lib')
    pr_links = {a['href'] for a in houseSoup('a') if 'press releases' in a.text.lower()}
    #print(f"{house_url}: {pr_links}")
    press_releases[house_url] = pr_links

print("Senate Press Releases: ")
#Get Press Releases for each senator
for s_url in good_senate_urls:
    html = requests.get(s_url).text
    senateSoup = BeautifulSoup(html, 'html5lib')
    pr_s_links = {a['href'] for a in senateSoup('a') if 'press releases' in a.text.lower()}
    print(f"{s_url}: {pr_links}")
    press_releases[s_url] = pr_s_links

#Now, get all press releases that mentions data
pr = []

for url, pr_link in press_releases.items():
    for link in pr_link:
        new_url = f"{url}/{link.replace(url, '')}"
        print(new_url)
        text = requests.get(new_url).text

        if paragraph_mentions(text, 'data'):
            #print(url + " " + new_url)
            pr.append(new_url)
            break

print(len(pr))
print("Done")