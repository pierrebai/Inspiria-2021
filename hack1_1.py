from helpers import *

import re

words_re = re.compile('''[a-zA-Z]+''')

freq = defaultdict(int)
for line in open('hack1.txt'):
    words = words_re.findall(line)
    words = map(lambda t: t.lower(), words)
    for w in words:
        w = w.strip()
        if not w:
            continue
        freq[w] += 1

freq = [(f,w) for w, f in freq.items()]

freq.sort()
print(len(freq))

words = [fw[1] for fw in freq]
words.reverse()

def is_prime(n):
    if n < 2: 
         return False
    if n % 2 == 0:             
         return n == 2
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

prime_words = []
for i, w in enumerate(words, 1):
    if is_prime(i):
        prime_words.append(w)

def w2i(w):
    total = 0
    for c in w:
        total = total * 36 + 10 + ord(c) - ord('a')
    return total

prime_words = list(map(w2i, prime_words))

prime_words.sort()

if len(prime_words) % 2 == 1:
    mid = len(prime_words) // 2
    median = prime_words[mid]
else:
    mid = len(prime_words) // 2
    median = (prime_words[mid-1], prime_words[mid], )

print(median)
