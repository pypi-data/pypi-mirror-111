def isalphanumeric(s):
    a=True
    for i in range(len(s)):
        if (ord(s[i])>=97 and ord(s[i])<=122) or (ord(s[i])>=65 and ord(s[i])<=90) or (ord(s[i])>=48 and ord(s[i])<=57):
            a=True
        else:
            a=False
    return a

def isalphabets(s):
    a=True
    for i in range(len(s)):
        if (ord(s[i])>=97 and ord(s[i])<=122) or (ord(s[i])>=65 and ord(s[i])<=90):
            a=True
        else:
            a=False
    return a

def isdigits(s):
    a=True
    for i in range(len(s)):
        if (ord(s[i])>=48 and ord(s[i])<=57):
            a=True
        else:
            a=False
    return a

def isuppers(s):
    a=True
    for i in range(len(s)):
        if (ord(s[i])>=65 and ord(s[i])<=90) or (ord(s[i])>=48 and ord(s[i])<=57) or (ord(s[i])>=32 and ord(s[i])<=47) or (ord(s[i])>=58 and ord(s[i])<=64) or (ord(s[i])>=91 and ord(s[i])<=96) or (ord(s[i])>=123 and ord(s[i])<=126):
            a=True
        else:
            a=False
    return a

def islowers(s):
    a=True
    for i in range(len(s)):
        if (ord(s[i])>=97 and ord(s[i])<=122) or (ord(s[i])>=48 and ord(s[i])<=57) or (ord(s[i])==32 and ord(s[i])<=47) or (ord(s[i])>=58 and ord(s[i])<=64) or (ord(s[i])>=91 and ord(s[i])<=96) or (ord(s[i])>=123 and ord(s[i])<=126):
            a=True
        else:
            a=False
    return a

def isspaces(s):
    a=True
    for i in range(len(s)):
        if (ord(s[i])==32):
            a=True
        else:
            a=False
    return a

def palindrome(s):
    b=[]
    j=len(s)-1
    for i in range(len(s)):
        b.append(s[j])
        j=j-1
    b=''.join(b)
    if s==b:
        return True
    else:
        return False

def pangram(s):
    s=s.lower()
    c=[]
    for i in s:
        if (i not in c) and (ord(i)>=97 and ord(i)<=122):
            c.append(i)
    if(len(c)==27 or len(c)==26):
        return True
    else:
        return False

def anagram(s,s1):
    a=[]
    b=[]
    for i in range(len(s)):
        a.append(ord(s[i]))
    for i in range(len(s1)):
        b.append(ord(s1[i]))
    if sum(a)==sum(b):
        return True
    else:
        return False
def alphaorder(s):
    a=[]
    b=[]
    for i in range(len(s)):
        a.append(ord(s[i]))
    a.sort()
    for i in range(len(s)):
        b.append(chr(a[i]))
    b=''.join(b)
    return b

def char_to_ascii(s):
    a=[]
    for i in range(len(s)):
        a.append(ord(s[i]))
    return a

def dec_to_char(s):
    a=[]
    for i in range(len(s)):
        a.append(chr(s[i]))
    a=''.join(a)
    return a
