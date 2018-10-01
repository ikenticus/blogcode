#!/usr/bin/python
import copy
import re

def get_json_cards(cards):
  # cards.copy() does not work because it is a collection and not a dict to .copy()
  # standard quick list[:] copy does not work because it will clone the objects as pointers
  #jcards = cards[:]
  # therefore, use the copy module function to .deepcopy()

  jcards = copy.deepcopy(cards)
  for card in jcards:
    card['path'] = re.sub(r'\.html', '.json', card['path'])
  return jcards

cards = []

cards.append( {'path': '/baby/shower.html'} )
cards.append( {'path': '/adult/birthday.html'} )
cards.append( {'path': '/get-together/sports.html'} )
cards.append( {'path': '/celebration/wedding.html'} )
cards.append( {'path': '/orgs/html_tutorial.html'} )

json_cards = get_json_cards(cards)


print "cards"
for card in cards:
  print card['path'] 

print "json cards"
for card in json_cards:
  print card['path']

