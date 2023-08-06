def length(s):
    count=0
    for i in range(len(s)):
        count=count+1
    return count

def uppercase(s):
    a=[]
    for i in range(len(s)):
        if (ord(s[i])>=97 and ord(s[i])<=122):
            a.append(chr(ord(s[i])-32))
        else:
            a.append(s[i])
    b=''.join(a)
    return str(b)

def lowercase(s):
    a=[]
    for i in range(len(s)):
        if (ord(s[i])>=65 and ord(s[i])<=90):
            a.append(chr(ord(s[i])+32))
        else:
            a.append(s[i])
    b=''.join(a)
    return str(b)

def title(s):
    count=0
    pos=[]
    for i in range(len(s)):
        if s[i]!=" " and s[i]!=".":
            count=count+1
        if s[i]==" " or s[i]==".":
            pos.append(count)
            count=count+1
    if ord(s[0])>=97 and ord(s[0])<=122:
        a=list(s)
        a[0]=chr(ord(s[0])-32)
        for i in range(len(pos)):
            a[pos[i]+1]=chr(ord(a[pos[i]+1])-32)
        b=''.join(a)
    if ord(s[0])>=65 and ord(s[0])<=90:
        a=list(s)
        for i in range(len(pos)):
            a[pos[i]+1]=chr(ord(a[pos[i]+1])-32)
        b=''.join(a)
    return b

def swapping_case(s):
    a=[]
    for i in range(len(s)):
        if (ord(s[i])>=97 and ord(s[i])<=122):
            a.append(chr(ord(s[i])-32))
        elif (ord(s[i])>=65 and ord(s[i])<=90):
            a.append(chr(ord(s[i])+32))
        else:
            a.append(s[i])
    a=''.join(a)
    return a

def starts(s,s1,pos):
    a=[]
    for i in range(len(s1)):
        a.append(s[pos])
        pos=pos+1
    b=''.join(a)
    if s1==b:
        return True
    else:
        return False

def spliting_lines(s):
    a=[]
    count=0
    for i in range(len(s)):
        if s[i]!=".":
            count=count+1
        if s[i]==".":
            a.append(count)
            count=count+1
    a.append(len(s))
    b=[]
    b.append(s[0:a[0]])
    for i in range(len(a)-1):
        b.append(s[a[i]+1:a[i+1]])
    if len(b)>1:
        while('' in b):
            b.remove('')
    return b

def counting_char(s,s1,start,end):
    count=0
    for i in range(len(s[start:end+1])):
        if s[i]==s1:
            count=count+1
    return count

def finding(s,s1,start,end):
    ss1=s[start:end+1]
    for i in range(len(ss1)):
        if ss1[i]==s1[0]:
            return i

def comparison(s,s1):
    if s==s1:
        return True
    else:
        return False

def concatenate(s,s1):
    a=[]
    a.append(s)
    for i in range(len(s1)):
        a.append(s1[i])
    b=''.join(a)
    return b

def copy(s):
    return s

def reverse(s):
    a=list(s)
    b=[]
    j=len(s)
    for i in range(len(s)):
        b.append(s[j-1])
        j=j-1
    b=''.join(b)
    return b

def replace(s,s1,s2):
    a=list(s)
    b=[]
    for i in range(len(s)):
        if s[i]==s1:
            b.append(i)
    for i in range(len(b)):
        a[b[i]]=s2
    c=''.join(a)
    return c

def capitalizes(s):
    a=list(s)
    if ord(a[0])>=65 and ord(a[0])<=90:
        pass
    if ord(a[0])>=97 and ord(a[0])<=122:
        a[0]=chr(ord(a[0])-32)
    a=''.join(a)
    return a

def multiply(s,n):
    a=[]
    for i in range(n):
        a.append(s)
    a=''.join(a)
    return a
