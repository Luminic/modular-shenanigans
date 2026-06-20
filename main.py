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

def main():
    a,b=2,3
    p=17
    for x in range(p):
        for y in range(p):
            G=(x,y)
            if not verify(G,a,b,p):
                continue
            l=np.zeros((p,p),dtype=np.uint8)
            brightness=200
            l[*G]=255
            A=G
            c=1
            while True:
                A=add(A,G,a,b,p)
                c+=1
                if math.isinf(A[1]):
                    break
                brightness*=.8
                l[*A]=int(brightness)+55
            print(c)
            cv2.imshow("test",cv2.resize(l,(800,800),interpolation=cv2.INTER_AREA))
            cv2.waitKey(0)

main()