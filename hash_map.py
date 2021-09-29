# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def sort_keys(tuple):
    return tuple[1]

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()
    list = []
    ht = HashMap(2500,hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                w = w.lower()                   # Ignore capitalization.
                cur_val = ht.get(w)             # Returns value at given key.
                if cur_val:
                    ht.put(w, cur_val + 1)      # Update hash map and increment word count at key.
                else:
                    ht.put(w, 1)                # Otherwise add it to hash map, start count at 1.
                    keys.add(w)                 # Add it to array of known words.
        for x in keys:
            list.append((x, ht.get(x)))         # Create tuples using key and value (using hash map's 'get').
        list.sort(reverse=True, key=sort_keys)  # Sort descending by number of occurrences.
    return list[0:number]                       # Return the list from 0 to [whatever].

def get_input():
    print('Please enter source file path:')
    source = input()
    print('Please enter number of top words to return:')
    number = input()
    return (source, int(number))

(source, number) = get_input()
word_list = top_words(source, number)
print('------------')

for x in range(len(word_list)):
    print(word_list[x][0], end='\t')
    print(word_list[x][1])
