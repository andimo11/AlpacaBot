import math

ymd = [2,0,1,9,1,2,3,1]
n = 0
for i in ymd:
    x = int(math.pow(i,2))
    n += x
j = chr(0x41 + n % 0x1a)
print(j)
