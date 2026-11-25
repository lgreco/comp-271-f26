# STUDENT REVIEW NOTES
# This script downloads a book, compresses it with our Huffman class, and
# reports how much space we saved. Things to notice:
#
#   * It is a SCRIPT, not a pytest test: there are no test_ functions and
#     no assert statements. Run it with  python test_huffman.py.
#     (If pytest collects this file, it will run the download on import
#     and then report that it found no tests.)
#   * It needs an internet connection and the third-party packages
#     "requests" and "pympler".
#   * It never checks that decoding gives back the original text. A
#     compressor that loses data is useless, so a good exercise is to add a
#     round-trip check at the bottom (see the suggestion there).

from __future__ import annotations  # for cool type hinting

# Install Pympler with: python -m pip install pympler
from pympler import asizeof # To measure size of dict()
import requests
from huffman import Huffman

ASCII_BITS = 8

# J Joyce's Ulysses is a long book, about 1.5 MB in clear text, 
# that we can use to test our encoder on a large message.  
long_book = "https://www.gutenberg.org/cache/epub/4300/pg4300.txt"

# Edgar Allen Poe's Cask of Amontillado is a short book, about 33 KB in size. 
# We can use it to test our encoder on a small message.
short_book = "https://www.gutenberg.org/cache/epub/1063/pg1063.txt"

source = long_book
message = requests.get(source, timeout=20).text

# Baseline: what the message costs if every character takes 8 bits.
# (Strictly, Python strings are Unicode and a few characters in a Gutenberg
# file may need more than 8 bits in UTF-8; 8 bits per character is the
# classic ASCII baseline used for comparison.)
ascii_length = len(message) * ASCII_BITS

huffman = Huffman(verbose=True)
encoded, tree = huffman.encode(message)

# Each character of `encoded` is "0" or "1", i.e. it represents ONE bit,
# so the length of the string is the size of the compressed data in bits.
encoded_length = len(encoded)
# The receiver needs the tree to decode, so a fair comparison must charge
# for it too. asizeof() reports the memory (in BYTES) used by the whole tree
# of Python objects, so we multiply by 8 to get bits.
# This is a very pessimistic estimate: Python objects carry a lot of
# overhead (object headers, dictionaries for attributes, pointers). A real
# file format would store just the k symbols and their frequencies, or even
# just each symbol's code length ("canonical Huffman codes"), which takes
# a few hundred bytes. For a short message, try to predict whether the
# overhead of the tree can make the "compressed" result BIGGER than the
# original -- then switch `source` to short_book and check.
encoder_size = asizeof.asizeof(tree) * ASCII_BITS

print(f"\nOriginal message length (in bits): {ascii_length:,d}")
print(f"Encoded message length (in bits): {encoded_length:,d}")
print(f"Encoder size (in bits): {encoder_size:,d}")
print(f"Total size of encoded message and encoder (in bits): {encoded_length + encoder_size:,d}")
print(f"Compression ratio: {ascii_length / (encoded_length + encoder_size):.2f}")

# Suggested round-trip check (uncomment to try). Every lossless compressor
# must satisfy decode(encode(x)) == x. Note that decoding is done by a
# brand-new Huffman object: all it needs is the encoded bits and the tree.
#
# decoded = Huffman().decode(encoded, tree)
# assert decoded == message, "Round trip failed: decoded text differs!"
# print("Round trip OK: decoded message matches the original.")
