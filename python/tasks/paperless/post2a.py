#!/usr/bin/python
import copy
import re

def get_json_cards(cards):
  jcards = copy.deepcopy(cards)
  for card in jcards:
    card['path'] = re.sub(r'html', 'json', card['path'])
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

'''
    If we alter the regex from \.html and remove the dot
    Will the code still work as expected?
'''

