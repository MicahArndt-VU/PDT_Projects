import datetime
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import random
random.seed((str) (datetime.datetime.now()))

def fix_unicode(text: str) -> str:
    return text.replace(u"â", "'")

#Generate Text using bigrams
def generate_using_bigrams(transitions) -> str:
    current = "." # this means the next word will start a sentence
    result = []
    while True:
        next_word_candidates = transitions[current]  # bigrams (current, _)
        current = random.choice(next_word_candidates)  # choose one at random
        result.append(current)  # append it to results
        if current == ".": return " ".join(result)  # if "." we're done

def generate_using_trigrams(transitions, starts):
    current = random.choice(starts)
    prev = "."
    result = [current]
    while True:
        next_word_candidates = transitions[(prev, current)]
        next_word = random.choice(next_word_candidates)
        prev, current = current, next_word
        result.append(current)

        if current == ".":
            return " ".join(result)
#Don't Use
def generate_using_quadgrams(transitions, starts, trigram_transitions):
    current = random.choice(starts)
    prev = "."
    nnext = ""
    #Get next value using trigram
    while True:
        t = trigram_transitions[(prev, current)]
        i = 0
        if len(t) > 1:
            i = (int) (random.randint(0, len(t)))
        nnext = t[i]
        if nnext == ".":
            continue
        else:
            break
    result = [current, nnext]
    #start finding transitions
    while True:
        #Get new candidates
        next_word_candidates = transitions[(prev, current, nnext)]
        #make sure that we have enough words to randomly select
        if len(next_word_candidates) > 1:
            next_word = next_word_candidates[random.randint(0, len(next_word_candidates))]
        else:
            if len(next_word_candidates) == 1:
                next_word = next_word_candidates[0]
            else: next_word = "."
        #Get new next value
        t = trigram_transitions[(current, nnext)]
        print("Current Transitions for next: ", t)
        i = 0
        if len(t) > 1:
            i = (random.randint(0, len(t)))
        elif len(t) == 1:
            i = 0
        if len(t) > 0:
            print(i, len(t))
            nnext = t[i]
        else:
            nnext = "."
        prev, current,nnext = current, nnext, next_word
        #print(prev, current, nnext)
        result.append(current)
        print(result)
        if current == "." or nnext == ".":
            if nnext == '.':
                result.append(nnext)
            return " ".join(result)

#Url used for training AI
url = "https://www.oreilly.com/ideas/what-is-data-science"
#make request
html = requests.get(url).text
#print(html)
soup = BeautifulSoup(html, 'html5lib')
#print(soup["div"])

content = soup.find("div", "main-post-radar-content") # find article-body div
regex = r"[\w']+|[\.]"      #Match a word or a period

document = []

for paragraph in content("p"):
    words = re.findall(regex, fix_unicode(paragraph.text))
    document.extend(words)

transitions = defaultdict(list)
for prev, current in zip(document, document[1:]):
    transitions[prev].append(current)

trigram_transitions = defaultdict(list)
starts = []

for prev, current, next in zip(document, document[1:], document[2:]):
    if prev == ".": # if the previous "word" was a period
        starts.append(current) # then this is a start word
    trigram_transitions[(prev, current)].append(next)

quadgram_transitions = defaultdict(list)
qgram_starts = []
for prev, curr, n1, n2 in zip(document, document[1:], document[2:], document[3:]):
    if prev == '.':
        qgram_starts.append(curr)
    quadgram_transitions[(prev,curr,n1)].append(n2)


print(generate_using_bigrams(transitions))
print()
print("Or said with Trigrams: ")
print()
print(generate_using_trigrams(trigram_transitions, starts))
print()


for i in range(5):
    print(generate_using_trigrams(trigram_transitions, starts))
