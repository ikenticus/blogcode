'''
    config: contains configurations that can easily be modifed and alter rolodex processing
'''
import re

'''
    valid_lines (name, zip5, phone10, color):
        First M., Last, 12345, 123 456 7890, color name
        Last, First, (123)-456-7890, color name, 12345
        First Last, color name, 12345, 123 456 7890

    complex regular expressions:
        First[ M.]: ([A-Z][a-z]+(?: [A-Z]\.)?)          # not using \s since that matched tabs, etc
        phone10: \(?(\d{3})\)?[- ](\d{3})[- ](\d{4})    # areacode - exchange(xc) - extension(ext)
        color name: ([a-zA-Z]{3,}(?: [a-zA-Z]{3,})?)    # assuming red is the shortest possible name
'''
valid_lines = (
    {
        'patt': re.compile('^([A-Z][a-z]+(?: [A-Z]\.)?), ([A-Z][a-z]+), (\d{5}), \(?(\d{3})\)?[- ](\d{3})[- ](\d{4}), ([a-zA-Z]{3,}(?: [a-zA-Z]{3,})?)$'),
        'list': ['firstname', 'lastname', 'zipcode', 'phonenumber', 'phone_xc', 'phone_ext', 'color']
    },
    {
        'patt': re.compile('^([A-Z][a-z]+), ([A-Z][a-z]+(?: [A-Z]\.)?), \(?(\d{3})\)?[- ](\d{3})[- ](\d{4}), ([a-zA-Z]{3,}(?: [a-zA-Z]{3,})?), (\d{5})$'),
        'list': ['lastname', 'firstname', 'phonenumber', 'phone_xc', 'phone_ext', 'color', 'zipcode']
    },
    {
        'patt': re.compile('^([A-Z][a-z]+(?: [A-Z]\.)?) ([A-Z][a-z]+), ([a-zA-Z]{3,}(?: [a-zA-Z]{3,})?), (\d{5}), \(?(\d{3})\)?[- ](\d{3})[- ](\d{4})$'),
        'list': ['firstname', 'lastname', 'color', 'zipcode', 'phonenumber', 'phone_xc', 'phone_ext']
    }
)

write_output = {
    'entries': [
        {
            'color': 'blue',
            'firstname': 'Foo',
            'lastname': 'Bar',
            'phonenumber': '800-555-1212',
            'zipcode': '10001'
        }
    ],
    'errors': [
        0
    ]
}

write_tests = (
    {
        'desc': 'Valid firstname',
        'key': 'firstname',
        'want': 'Foo',
    },
    {
        'desc': 'Valid lastname',
        'key': 'lastname',
        'want': 'Bar',
    },
    {
        'desc': 'Valid color',
        'key': 'color',
        'want': 'blue',
    },
    {
        'desc': 'Valid phone',
        'key': 'phonenumber',
        'want': '800-555-1212',
    },
    {
        'desc': 'Valid zip',
        'key': 'zipcode',
        'want': '10001',
    },
)

valid_wants = {
    'empty': {},
    'first+color': {
        'color': 'color',
        'firstname': 'First',
        'lastname': 'Last',
        'phonenumber': '123-456-7890',
        'zipcode': '12345',
    },
    'middle+color': {
        'color': 'color',
        'firstname': 'First M.',
        'lastname': 'Last',
        'phonenumber': '123-456-7890',
        'zipcode': '12345',
    },
    'first+color2': {
        'color': 'color name',
        'firstname': 'First',
        'lastname': 'Last',
        'phonenumber': '123-456-7890',
        'zipcode': '12345',
    },
    'middle+color2': {
        'color': 'color name',
        'firstname': 'First M.',
        'lastname': 'Last',
        'phonenumber': '123-456-7890',
        'zipcode': '12345',
    },
}

parse_tests = (
    {
        'desc': 'Valid first,last with spaced phone and color',
        'line': 'First, Last, 12345, 123 456 7890, color',
        'want': valid_wants['first+color'],
    },
    {
        'desc': 'Valid first+middle,last with spaced phone and color',
        'line': 'First M., Last, 12345, 123 456 7890, color',
        'want': valid_wants['middle+color'],
    },
    {
        'desc': 'Valid first,last with spaced phone and spaced color',
        'line': 'First, Last, 12345, 123 456 7890, color name',
        'want': valid_wants['first+color2'],
    },
    {
        'desc': 'Valid first+middle,last with spaced phone and spaced color',
        'line': 'First M., Last, 12345, 123 456 7890, color name',
        'want': valid_wants['middle+color2'],
    },
    {
        'desc': 'Valid first,last with (phone) and color',
        'line': 'First, Last, 12345, (123) 456-7890, color',
        'want': valid_wants['first+color'],
    },
    {
        'desc': 'Valid first+middle,last with (phone) and color',
        'line': 'First M., Last, 12345, (123) 456-7890, color',
        'want': valid_wants['middle+color'],
    },
    {
        'desc': 'Valid first,last with (phone) and spaced color',
        'line': 'First, Last, 12345, (123) 456-7890, color name',
        'want': valid_wants['first+color2'],
    },
    {
        'desc': 'Valid first+middle,last with (phone) and spaced color',
        'line': 'First M., Last, 12345, (123) 456-7890, color name',
        'want': valid_wants['middle+color2'],
    },

    {
        'desc': 'Valid last,first with spaced phone and color',
        'line': 'Last, First, 123 456 7890, color, 12345',
        'want': valid_wants['first+color'],
    },
    {
        'desc': 'Valid last,first+middle with spaced phone and color',
        'line': 'Last, First M., 123 456 7890, color, 12345',
        'want': valid_wants['middle+color'],
    },
    {
        'desc': 'Valid last,first with spaced phone and spaced color',
        'line': 'Last, First, 123 456 7890, color name, 12345',
        'want': valid_wants['first+color2'],
    },
    {
        'desc': 'Valid last,first+middle with spaced phone and spaced color',
        'line': 'Last, First M., 123 456 7890, color name, 12345',
        'want': valid_wants['middle+color2'],
    },
    {
        'desc': 'Valid last,first with (phone) and color',
        'line': 'Last, First, (123)-456-7890, color, 12345',
        'want': valid_wants['first+color'],
    },
    {
        'desc': 'Valid last,first+middle with (phone) and color',
        'line': 'Last, First M., (123)-456-7890, color, 12345',
        'want': valid_wants['middle+color'],
    },
    {
        'desc': 'Valid last,first with (phone) and spaced color',
        'line': 'Last, First, (123)-456-7890, color name, 12345',
        'want': valid_wants['first+color2'],
    },
    {
        'desc': 'Valid last,first+middle with (phone) and spaced color',
        'line': 'Last, First M., (123)-456-7890, color name, 12345',
        'want': valid_wants['middle+color2'],
    },

    {
        'desc': 'Valid first last with spaced phone and color',
        'line': 'First Last, color, 12345, 123 456 7890',
        'want': valid_wants['first+color'],
    },
    {
        'desc': 'Valid first+middle last with spaced phone and color',
        'line': 'First M. Last, color, 12345, 123 456 7890',
        'want': valid_wants['middle+color'],
    },
    {
        'desc': 'Valid first last with spaced phone and spaced color',
        'line': 'First Last, color name, 12345, 123 456 7890',
        'want': valid_wants['first+color2'],
    },
    {
        'desc': 'Valid first+middle last with spaced phone and spaced color',
        'line': 'First M. Last, color name, 12345, 123 456 7890',
        'want': valid_wants['middle+color2'],
    },
    {
        'desc': 'Valid first last with (phone) and color',
        'line': 'First Last, color, 12345, (123) 456-7890',
        'want': valid_wants['first+color'],
    },
    {
        'desc': 'Valid first+middle last with (phone) and color',
        'line': 'First M. Last, color, 12345, (123) 456-7890',
        'want': valid_wants['middle+color'],
    },
    {
        'desc': 'Valid first last with (phone) and spaced color',
        'line': 'First Last, color name, 12345, (123) 456-7890',
        'want': valid_wants['first+color2'],
    },
    {
        'desc': 'Valid first+middle last with (phone) and spaced color',
        'line': 'First M. Last, color name, 12345, (123) 456-7890',
        'want': valid_wants['middle+color2'],
    },

    {
        'desc': 'Invalid color',
        'line': 'First M. Last, re gex, 12345, (123) 456-7890',
        'want': valid_wants['empty'],
    },
    {
        'desc': 'Invalid name',
        'line': 'First Last III, color, 12345, (123) 456-789',
        'want': valid_wants['empty'],
    },
    {
        'desc': 'Invalid zip',
        'line': 'First M. Last, color, 123456789, (123) 456-789',
        'want': valid_wants['empty'],
    },
    {
        'desc': 'Invalid phone',
        'line': 'First M. Last, color, 12345, (123) 456-789',
        'want': valid_wants['empty'],
    },
    {
        'desc': 'Invalid zip',
        'line': 'First M. Last, color, 123456789, (123) 456-789',
        'want': valid_wants['empty'],
    },
)
