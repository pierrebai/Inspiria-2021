words = (1300555140, 23069098741)

median = (words[0] + words[1]) // 2
print(median)

from hashlib import sha256

s256 = sha256(str(median).encode('ascii')).hexdigest()
print(s256[0:13])
    
