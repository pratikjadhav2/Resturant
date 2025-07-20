from functools import reduce
l = [10,20,30,40]
sum = reduce(lambda x,y:x+y,l)
print(sum)