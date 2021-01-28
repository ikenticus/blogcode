
"""
We are working on a security system for a badged-access room in our company's building.

Given an ordered list of employees who used their badge to enter or exit the room, write a function that returns two collections:

1. All employees who didn't use their badge while exiting the room - they recorded an enter without a matching exit. (All employees are required to leave the room before the log ends.)

2. All employees who didn't use their badge while entering the room - they recorded an exit without a matching enter. (The room is empty when the log begins.)

Each collection should contain no duplicates, regardless of how many times a given employee matches the criteria for belonging to it.

badge_records_1 = [
  ["Martha",   "exit"],
  ["Paul",     "enter"],
  ["Martha",   "enter"],
  ["Martha",   "exit"],
  ["Jennifer", "enter"],
  ["Paul",     "enter"],
  ["Curtis",   "exit"],
  ["Curtis",   "enter"],
  ["Paul",     "exit"],
  ["Martha",   "enter"],
  ["Martha",   "exit"],
  ["Jennifer", "exit"],
  ["Paul",     "enter"],
  ["Paul",     "enter"],
  ["Martha",   "exit"],
]

Expected output: ["Curtis", "Paul"], ["Martha", "Curtis"]

Additional test cases:

badge_records_2 = [
  ["Paul", "enter"],
  ["Paul", "enter"],
  ["Paul", "exit"],
]

Expected output: ["Paul"], []

badge_records_3 = [
  ["Paul", "enter"],
  ["Paul", "exit"],
  ["Paul", "exit"],
]

Expected output: [], ["Paul"]

badge_records_4 = [
  ["Paul", "exit"],
  ["Paul", "enter"],
  ["Martha", "enter"],
  ["Martha", "exit"],
]

Expected output: ["Paul"], ["Paul"]

badge_records_5 = [
  ["Paul", "enter"],
  ["Paul", "exit"],
]

Expected output: [], []

badge_records_6 = [
  ["Paul", "enter"],
  ["Paul", "enter"],
  ["Paul", "exit"],
  ["Paul", "exit"],
]

Expected output: ["Paul"], ["Paul"]

"""

badge_records_1 = [
  ["Martha",   "exit"],
  ["Paul",     "enter"],
  ["Martha",   "enter"],
  ["Martha",   "exit"],
  ["Jennifer", "enter"],
  ["Paul",     "enter"],
  ["Curtis",   "exit"],
  ["Curtis",   "enter"],
  ["Paul",     "exit"],
  ["Martha",   "enter"],
  ["Martha",   "exit"],
  ["Jennifer", "exit"],
  ["Paul",     "enter"],
  ["Paul",     "enter"],
  ["Martha",   "exit"],
]

badge_records_2 = [
  ["Paul", "enter"],
  ["Paul", "enter"],
  ["Paul", "exit"],
]

badge_records_3 = [
  ["Paul", "enter"],
  ["Paul", "exit"],
  ["Paul", "exit"],
]

badge_records_4 = [
  ["Paul", "exit"],
  ["Paul", "enter"],
  ["Martha", "enter"],
  ["Martha", "exit"],
]

badge_records_5 = [
  ["Paul", "enter"],
  ["Paul", "exit"],
]

badge_records_6 = [
  ["Paul", "enter"],
  ["Paul", "enter"],
  ["Paul", "exit"],
  ["Paul", "exit"],
]

def check_user(user, status):
    if user not in user_state.keys():
        user_state[user] = 0
    if status == 'enter':
        if user_state[user] >= 1:
            extra_enter.append(user)
        else:
            user_state[user] += 1
    elif status == 'exit':
        if user_state[user] <= 0:
            extra_exit.append(user)
        else:
            user_state[user] -= 1
    # print(user_state, extra_enter, extra_exit)

def check_room(room):
    global extra_exit
    global extra_enter
    global user_state
    extra_exit = []
    extra_enter = []
    user_state = {}

    # check records for room
    for badge in room:
        check_user(badge[0], badge[1])

    # check nobody in room
    for user in user_state.keys():
        if user_state[user] > 0:
            extra_enter.append(user)
    return list(set(extra_enter)), list(set(extra_exit))

print(check_room(badge_records_1))
print(check_room(badge_records_2))
print(check_room(badge_records_3))
print(check_room(badge_records_4))
print(check_room(badge_records_5))
print(check_room(badge_records_6))

'''

Expected output: ["Curtis", "Paul"], ["Martha", "Curtis"]
Expected output: ["Paul"], []
Expected output: [], ["Paul"]
Expected output: ["Paul"], ["Paul"]
Expected output: [], []
Expected output: ["Paul"], ["Paul"]

(['Curtis', 'Paul'], ['Curtis', 'Martha'])
(['Paul'], [])
([], ['Paul'])
(['Paul'], ['Paul'])
([], [])
(['Paul'], ['Paul'])

'''
