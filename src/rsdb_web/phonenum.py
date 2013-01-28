#!/usr/bin/env python

import re

non_numeric_plus = re.compile(r"[^0-9+]+")

def canonicalise(s):
    if s is None:
        return None
    
    s = non_numeric_plus.sub("", s)
    groups = []
    i = 0
    while True:
        print i
        start = len(s) - i - 4
        if start < 0:
            start = 0
        four_digits = s[start : len(s) - i]
        groups.append(four_digits)
        i += 4
        if i > len(s):
            break
    groups.reverse()
    if "" in groups: groups.remove("")
    tmp = " ".join(groups)
    tmp = tmp.replace("+ ", "+")
    return tmp
