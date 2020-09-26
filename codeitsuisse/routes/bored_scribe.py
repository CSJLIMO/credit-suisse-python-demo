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
    

@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored_scribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    op = []
    for item in data:
        encoded = item["encryptedText"]
        decoded = decode(encoded)
        encode_key = get_key(decoded)
        
        count = -1
        temp = decoded
        for i in range(26):
            if temp == encoded:
                count = i
                break
            temp = shift_k(temp, encode_key)
        
        
        op.append({"id": item["id"], "encryptionCount": count, "originalText": decoded})
        

    logging.info("My result :{}".format(op))
    return jsonify(op);










