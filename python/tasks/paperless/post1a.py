#!/usr/bin/python
import re

def get_json_cards(cards):
  for card in cards:
    card['path'] = re.sub(r'html$', 'json', card['path'])
  return cards

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
    There is a bug in this code, can you find it and fix it?
'''

