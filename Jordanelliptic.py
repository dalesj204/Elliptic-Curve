from __future__ import print_function


N = 182755680224874988969105090392374859247
# N = 2
A = 286458106491124997002528249079664631375
# A = 1
P = 231980187997634794246138521723892165531
# P = 23

def inverse(a,b):
    prime = a
    x_pre, x = 1, 0;
    y_pre, y = 0, 1;

    while b:
        q, r = divmod(a,b)
        x, x_pre = x_pre - q*x, x
        y, y_pre = y_pre - q*y, y        
        a = b
        b = r
    if y_pre < 0 :
        y_pre = prime + y_pre
    return y_pre 

def same_pts(x, y):
    numerator = (3*pow(x, 2) + A)
    denom = (2*y) % P
    invY = inverse(P,denom)
    m = (numerator * invY) % P
    
    xR = (pow(m, 2) - (2*x)) % P
    yR = (y + m*(xR-x)) % P

    return xR, P-yR


def diff_pts(xP, yP, xQ, yQ):
    num = (yQ - yP) # numerator
    denom = (xQ - xP) % P # denominator
    invX = inverse(P, denom) # now take the inverse of the denominator
    m = (num * invX) % P
    
    xR = (pow(m, 2) -xP -xQ) % P
    yR = (yP + m*(xR-xP)) % P

    return xR, P-yR

def multiplier(x, y, N):
    # if N == 1:
    #     return x, y
    # if N % 2 == 0:
    #     tempX, tempY = multiplier(x, y, N//2)
    #     newX, newY = same_pts(tempX, tempY)
    # else:
    #     tempX, tempY = multiplier(x, y, (N - 1)//2)
    #     temp2X, temp2Y = same_pts(tempX, tempY)
    #     newX, newY = diff_pts(temp2X, temp2Y, x, y)
    # return newX, newY
    if N == 1:
        return x, y
    elif N == 2:
        return same_pts(x, y)
    elif N % 2 == 1:
        return diff_pts(x, y, *multiplier(x, y ,N-1))
    else:
        return same_pts(*multiplier(x, y, N/2))


f = open('a4.cipher', 'r')
f2 = open('msg.txt', 'w+')
lines = f.readlines()
list = []

for line in lines:
    split_line = line.split(' ')
    xC = long(split_line[0]) # x-coordinate of cipher
    # print("xC: " + str(xC))
    yC = long(split_line[1]) # y-coordinate of cipher
    # print("yC: " + str(yC))
    xH = long(split_line[2]) # x-coordinate of half mask
    # print("xH: " + str(xH))
    yH = long(split_line[3]) # y-coordinate of half mask
    # print("yH: " + str(yH))
       
    
    xF, yF = multiplier(xH, yH, N) # full mask
    msgX, _ = diff_pts(xC, yC, xF, P-yF)
    list.append(msgX)

    
for x in range(len(list)):
    f2.write(str(chr(list[x])))