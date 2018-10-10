'''
    code review was done on company laptop so this problem is not verbatim
    but is a reconstruction based on my memory several hours after the fact

    given the following code to check if two words are anagrams of each other
    refactor the code (keeping the while loops) to make clearer and more performant

> print is_anagram('abba', 'aabb')
True
> print is_anagram('abba', 'wxyz')
False

'''

def is_anagram(word_1, word_2):
    position_1 = 0
    still_ok = True

    while position_1 < len(word_1) and still_ok:
        letters_of_word_2 = list(word_2)

        position_2 = 0
        found = False

        while position_2 < len(letters_of_word_2) and not found:
            if word_1[position_1] == letters_of_word_2[position_2]:
                found = True
            else:
                position_2 = position_2 + 1
            
        if found:
            letters_of_word_2[position_2] = None
        else:
            still_ok = False

        position_1 = position_1 + 1
    return still_ok

print is_anagram('abba', 'aabb')
print is_anagram('abba', 'wxyz')


'''
    deleting word2 letters
'''

def is_anagram1(word_1, word_2):
    position_1 = 0
    still_ok = True

    while position_1 < len(word_1) and still_ok:
        letters_of_word_2 = list(word_2)

        position_2 = 0
        found = False

        while position_2 < len(letters_of_word_2) and not found:
            if word_1[position_1] == letters_of_word_2[position_2]:
                # del letters_of_word_2[position_2]
                letters_of_word_2.remove(letters_of_word_2[position_2])
                found = True
            else:
                position_2 += 1
            
        if not found:
            still_ok = False

        position_1 += 1
    return still_ok

print is_anagram1('abba', 'aabb')
print is_anagram1('abba', 'wxyz')

