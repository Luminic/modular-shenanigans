def mul(a,b,m):
    if b<a:
        a,b=b,a
    r=0
    while a>0:
        if a&1:
            r=(r+b)%m
        a>>=1
        b=(b<<1)%m
    return r

def pow(a,b,m):
    b%=m-1
    p=1
    while b!=0:
        if b%2==1:
            p=mul(p,a,m)
        b>>=1
        a=mul(a,a,m)
    return p

def div(a,b,m):
    return mul(a,minv(b,m),m)

def minv(a,m):
    b=m
    q=[]
    # euclidian algorithm
    while a!=1:
        q.append(b//a)
        b,a=a,b%a
    # extended euclidian algorithm
    a,b=0,1

    while len(q)!=0:
        a,b=b,(a-mul(b,q.pop(-1),m))%m
    return b



import math

def add(A,B,a,b,m):
    ax,ay=A
    bx,by=B
    if math.isinf(ay):
        return B
    if math.isinf(by):
        return A
    if A==B:
        return double(A,a,b,m)
    if ax==bx:
        return (0,math.inf)
    s=div((by-ay)%m,(bx-ax)%m,m)
    x=(mul(s,s,m)-ax-bx)%m
    y=(mul(s,(ax-x)%m,m)-ay)%m
    return (x,y)

def double(A,a,b,m):
    ax,ay=A
    if math.isinf(ay):
        return A
    if ay==0:
        return (0,math.inf)
    s=div((3*mul(ax,ax,m)+a)%m,(2*ay)%m,m)
    x=(mul(s,s,m)-2*ax)%m
    y=(mul(s,(ax-x)%m,m)-ay)%m
    return (x,y)

def scalar(A,k,a,b,m):
    R=(0,math.inf)
    while k>0:
        if k&1:
            R=add(R,A,a,b,m)
        k>>=1
        A=double(A,a,b,m)
    return R

def verify(A,a,b,m):
    ax,ay=A
    return math.isinf(ay) or mul(ay,ay,m)==(mul(mul(ax,ax,m),ax,m)+mul(a,ax,m)+b)%m

import cv2
import numpy as np
import random

def find_secret_key(G,Key1,Key2,a,b,m):
    A=G
    c=1
    while Key1!=A and Key2!=A:
        A=add(A,G,a,b,m)
        c+=1
    if Key1==A:
        print(scalar(Key2,c,a,b,m))
    else:
        print(scalar(Key1,c,a,b,m))

def find_valid(a,b,m):
    if m%4==3:
        while True:
            x=random.randint(0,m)
            ex=(pow(x,3,m)+mul(a,x,m)+b)%m
            if 1==pow(ex,m//2,m):
                y=pow(ex,(m+1)//4,m)
                if verify((x,y),a,b,m):
                    return (x,y)

def main():
    a,b=124819,1234512
    p=10000019
    G=find_valid(a,b,p)
    print(verify(G,a,b,p))
    secret_key=random.randint(0,p)
    my_key=random.randint(0,p)
    what_you_send_me=scalar(G,secret_key,a,b,p)
    print(what_you_send_me)
    what_i_send_you=scalar(G,my_key,a,b,p)
    print(what_i_send_you)
    your_shared_key=scalar(what_i_send_you,secret_key,a,b,p)
    my_shared_key=scalar(what_you_send_me,my_key,a,b,p)
    print("Secret from onlookers")
    print(your_shared_key)
    print(my_shared_key)
    find_secret_key(G,what_i_send_you,what_you_send_me,a,b,p)

main()