# STUDENT REVIEW NOTES
# This is the stand-alone warm-up version of step 1 of Huffman coding:
# counting how many times each symbol appears. The same logic lives inside
# Huffman.__count_frequencies in huffman.py.
#
# Pattern: "count with a dictionary." For each item, either increment its
# existing count or start it at 1. It runs in O(n) time for a message of
# n characters, since each dictionary check/update is O(1) on average.
#
# Equivalent one-liners you will see in real Python code:
#     frequency[char] = frequency.get(char, 0) + 1     # inside the loop
#     from collections import Counter; Counter(message) # the whole function
#
# Example: count_freq("hello") -> {'h': 1, 'e': 1, 'l': 2, 'o': 1}

def count_freq(message:str):
    frequency = dict()
    for char in message:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency