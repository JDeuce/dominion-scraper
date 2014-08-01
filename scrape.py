#!/usr/bin/env python

import codecs
import json
import urllib
import lxml.html

URL_BASE='http://dominionstrategy.com/card-decks/'
COLUMNS = ['Title', 'Type', 'Cost', 'Description']
decks = [
'dominion',
'intrigue',
'seaside',
'alchemy',
'prosperity',
'cornucopia',
'hinterlands',
'dark-ages',
'guilds'
]

cards = []
for deck in decks:
    print deck
    deck_url = "%s-card-list" % deck
    url = URL_BASE + deck_url
    f = urllib.urlopen(url)
    content = f.read()
    root = lxml.html.fromstring(content)
    rows = root.cssselect(".entry-content tr")
    for row in rows:
        data = {
            'Deck': deck
        }
        columns = row.cssselect("td")
        print "-- ", columns[0].text_content()
        try:
            for i, col in enumerate(COLUMNS):
                data[col] = columns[i].text_content().strip()
                if not data[col]:
                    raise Exception

        except:
            break
        else:
            cards.append(data)

with open("cards.json", "w") as f:
    f.write(json.dumps(cards))


with codecs.open("cards.csv", "w", "utf-8") as f:
    for card in sorted(cards, key=lambda c: (c['Deck'], c['Title'])):
        s = "%s,%s,%s,%s" % (card['Deck'], card['Title'], card['Type'], card['Cost'])
        f.write(s)
        f.write("\n")
