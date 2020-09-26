import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def is_vow(x):
    if x in ['a', 'e', 'i', 'o', 'u']:
        return 1
    return 0

def next_alpha_k(x, k):
    k = (k % 26 + 26) % 26
    if ord(x) + k > ord('z'):
        return chr(ord(x) + k - 26)
    return chr(ord(x) + k)

def shift_k(s, k):
    t = ""
    for c in s:
        t += next_alpha_k(c, k)
    return t

def get_score(s):
    now = 1
    ret = 0
    for i in range(1, len(s)):
        if is_vow(s[i]) == is_vow(s[i-1]):
            now += 1
        else:
            ret += now ** 2
            now = 1
    ret += now ** 2
    return ret

def decode(s):
    best_score = get_score(s)
    best_str = s
    for i in range(25):
        s = shift_k(s, 1)
        sc = get_score(s)
        if sc < best_score:
            best_score = sc
            best_str = s
    return best_str

def get_key(s):
    key = 0
    longest = str(s[0])
    n = len(s)
    for i in range(n):
        can = 0
        while True:
            if 0<=i-(can+1) and i+(can+1)<n and s[i-(can+1)] == s[i+(can+1)]:
                can += 1
            else:
                break
        key += can
        if len(longest) < 2*can+1:
            longest = s[(i-can):(i+can+1)]
    
    for i in range(n-1):
        if s[i] == s[i+1]:
            can = 0
            while True:
                if 0<=i-(can+1) and i+(can+2)<n and s[i-(can+1)] == s[i+(can+2)]:
                    can += 1
                else:
                    break
            key += (can + 1)
            if len(longest) < 2*can+2:
                longest = s[(i-can):(i+can+2)]        
    
    if len(longest) == 1:
        key = ord(s[0])
    else:
        for c in longest:
            key += ord(c)
    return key

f = open("words_10000.txt",'r')
lines = f.readlines()
words = []
for i in range(len(lines)-1):
    if len(lines[i][:-1]) >= 3:
        words.append(lines[i][:-1])
words.append(lines[len(lines)-1])
small_list = ["a", "ad", "am", "an", "as", "at", "ax", "be", "by", "do", "go", "if", "in", 
"is", "it", "me", "my", "no", "of", "on", "or", "ox", "so", "to", "us", "we"]
for word in small_list:
    words.append(word)
    
def is_valid(s):
    if s in words:
        return True
    n = len(s)
    if n>=6:
        return True
    return False    

def split_text(s):
    
    n = len(s)
    subwords = []
    for word in words:
        if s.find(word) != -1:
            subwords.append(word)            
    subwords.sort(key=len, reverse=True)
    
    ret = []

    splitted = False
    for word in subwords:
        st = s.find(word)
        en = st + len(word) - 1
        if (st == 0 or is_valid(s[:st])) and (en == n-1 or is_valid(s[(en+1):])):
            
            if st > 0:
                ret += split_text(s[:st])
            # print(" ", end = "")
            # print(word, end = "")
            ret += [word]
            # print(" ", end = "")
            if en < n-1:
                ret += split_text(s[(en+1):])
            splitted = True
            break
    if not splitted:
        ret += [s]
    return ret
    

@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored_scribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    op = []
    for item in data:
        encoded = item["encryptedText"]
        decoded = decode(encoded)
        
        count = -1
        temp = decoded
        for i in range(26):
            if temp == encoded:
                count = i
                break
            temp = shift_k(temp, get_key(temp))
            
        splitted = split_text(decoded)
        ds = splitted[0]
        for i in range(1, len(splitted)):
            ds = ds + ' ' + splitted[i]
        
        
        op.append({"id": item["id"], "encryptionCount": count, "originalText": ds})
        

    logging.info("My result :{}".format(op))
    return jsonify(op);


















