'''
    code review was done on company laptop so this problem is not verbatim
    but is a reconstruction based on my memory several hours after the fact

    suppose you open an ice cream store and every day you mark down just which flavors were
    with the given menu and the sales flavors, output a list of the sold flavors in same order of the menu
    do not mutate the original menu/sales lists

    menu = ['Vanilla', 'Chocolate', 'Strawberry', 'Banana', 'Neopolitan']
    sales = ['Chocolate', 'Strawberry', 'Neopolitan', 'Chocolate', 'Strawberry', 'Chocolate']
    output = ['Chocolate', 'Chocolate', 'Chocolate', 'Strawberry', 'Strawberry', 'Neopolitan']
'''

def icecream(menu, sales):
    # your code here
    pass

menu = ['Vanilla', 'Chocolate', 'Strawberry', 'Banana', 'Neopolitan']
sales = ['Chocolate', 'Strawberry', 'Neopolitan', 'Chocolate', 'Strawberry', 'Chocolate']


'''
    first attempt was O(N2)
'''

def icecream_N2(menu, sales):
    output = []
    for m in menu:
        for s in sales:
            if s == m:
                output.append(m)
    return output

print icecream_N2(menu, sales)


'''
    second attempt was O(2N) ?
'''

def icecream_2N(menu, sales):
    output = []
    orders = { m: 0 for m in menu }
    for s in sales:
        orders[s] += 1
    for m in menu:
        output.extend([ m for _ in range(orders[m]) ])
    return output

print icecream_2N(menu, sales)

