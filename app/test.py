
import itertools
a = (1, 2,3,4,5,6,7)
b = ('1')

c = itertools.product(a,b)
for i in c:
    print(i,end=",")