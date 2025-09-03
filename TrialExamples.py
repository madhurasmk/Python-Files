#b = 79
# a = 90 if b >= 80 else 10
# print(a)
import numpy as np
import pandas as pd
a = [1, 3, 6]
b = ['sf', 'sd', 'mm']
df = pd.DataFrame([[a, b,a]])
print(df)
print("-"*20)
df1 = pd.DataFrame([a,b,a])
print(df1)
print("-"*20)
df2 = pd.DataFrame({'A':a, 'B':b})
print(df2)
print("-"*20)

from readonly import readonly
@readonly
class Constants:
    MY_CONST = 10
    STR_CONST = "Hello"
# Constants.MY_CONST = 90   # AttributeError: can't set attribute
print(Constants.MY_CONST)
print(Constants.STR_CONST)

name = "Abc"
age = 29
greeting = "Hello {},  you are {} years old".format(name, age)
print(greeting)
greet1 = f"Hello {name},  you are {age} years old"
print(greet1)
print("This is a backslash: \\")

str_single_Quotes = "I said 'Hello'"
print(str_single_Quotes)
str_double_Quotes = 'I said "Hello"'
print(str_double_Quotes)
print(1//3)
print(1/3)
print(1%3)
str_esc_single_Quotes = "I\'m fine"
print(str_esc_single_Quotes)
str_esc_double_Quotes = "She said, It\'s raining"
print(str_esc_double_Quotes)
[a, b, c] = [1, 2, 3]
print("a:" , a, "b:", b, "c:", c)
x, y, z = 10, 20 , 30
print("x:" , x, "y:", y, "z:", z)

first, *rest = [1, 2, 3, 4, 5]
print("first:", first)
print("rest:", rest)

p = 40
q = 50
print(p, q)
p, q = q, p
print(p, q)

a = [1, 2, "Strin",3 ,5 , 6,7]
print(a)

print(a[1::2])
def names_deco(function):
    def wrapper(a1, a2):
        a1 = a1.upper()
        a2 = a2.capitalize()
        str_Hello = function(a1, a2)
        return str_Hello
    return wrapper
@names_deco
def sayHello(n1, n2):
    return 'Hello ' + n1 + '! Hello ' + n2 + '!'
print(sayHello('madhura', 'mulimani'))


mul = lambda a, b: a*b
print(mul(5, 10))

def myWrapper(n):
    return lambda a:a*n
mul1 = myWrapper(7)
print(mul1(5))

def multiply (a, b, *argv):
    mul = a * b
    for n in argv:
        mul *= n
    return mul
print(multiply(1, 2, 4))

def tellArgs(**kwargs):
    for k, v in kwargs.items():
        print(k + " : " + v)

tellArgs(a = "A", b = "B",  z = "Zee")

# Iterators in Python
class ArrList:
    def __init__(self, nlist):
        self.nos = nlist
    def __iter__(self):
        self.pos = 0
        return self
    def __next__(self):
        if (self.pos < len(self.nos)):
            self.pos +=1
            return self.nos[self.pos - 1]
        else:
            raise StopIteration

arrObj = ArrList([1,2,3])
it = iter(arrObj)
print(next(it))
print(next(it))
print(next(it))
# print(next(it))
# Arguments - passed by reference in Python

def appendNo(arr):
    arr.append(5)
arr = [1,2,3]
print(arr)
appendNo(arr)
print(arr)

def fib(n):
    p, q = 0, 1
    while (p<n):
        yield p
        p, q = q, p+q
x = fib(10)
# x.__next__()
# x.__next__()
# x.__next__()
# x.__next__()
# print(x.__next__())
for i in fib(56):
    print(i)

# xrange - returns xrange obj (deprecated) ; range - returns list. Both gen a seq of ints
for i in range(10):
    print(i)
for i in range(1, 5):
    print(i)

# Shallow copy
from copy import copy, deepcopy
lst1 = [1, 2, [3, 5], 4]
lst1_2 = copy(lst1)
lst1_2[3] = 7
lst1_2[2].append(6)
print(lst1_2)
print(lst1)

lst1_3 = deepcopy(lst1)
lst1_3[3] = 8
lst1_3[2].append(7)
print(lst1_3)
print(lst1)

# OOPS
class Parent(object):
    pass
class Child(Parent):
    pass
print(issubclass(Child, Parent))
print(issubclass(Parent, Child))
o1 = Child()
o2 = Parent()
print(isinstance(o2, Child))
print(isinstance(o2, Parent))


class EmpDemo:
    pass
e1 = EmpDemo()
e1.name = "Hello"
print(e1.name)

# protected : _ ; private : __
class Employee:
    _emp_name = None
    _emp_age = None
    __branch = None
    def __init__(self, name, age, branch):
        self._emp_name = name
        self._emp_age = age
        self.__branch = branch
    def display(self):
        print(self._emp_name + " : " + self._emp_age + " : " + self.__branch)
emp1 = Employee("Madhu", 48, "CS")
# print(emp1.display())

df11 = pd.Series([2, 4,6 , 8, 10])
df22 = pd.Series([8, 12, 16, 18])
df11 = df11[~df11.isin(df22)]
print(df11) # Gets items from series df11 that are not present in df22


# union and intersection
df12 = pd.Series([2, 4, 5, 8, 10])
df13 = pd.Series([8, 10, 13, 15, 17])
p_union = pd.Series(np.union1d(df12, df13))
p_intersect = pd.Series(np.intersect1d(df12, df13))
unique_elems = p_union[~p_union.isin(p_intersect)]
print(unique_elems)

dict_info = {'key1' : 2.0, 'key2' : 3.1, 'key3' : 2.2}
series_obj = pd.Series(dict_info)
print (series_obj)

dataframe = pd.DataFrame( df12, index=[0, 1,4], columns=["a"])
print(dataframe)

arr1 = [1, 3,5, 7]
revArr = arr1[::-1]
print(revArr)

arr = np.array([[8, 3, 2],
          [3, 6, 5],
          [6, 1, 4]])
arr = arr[arr[:, 0].argsort()]
print(arr)

inputArray = np.array([[35,53,63],[72,12,22],[43,84,56]])
new_col = np.array([[20,30,40]])
arrDel = np.delete(inputArray, 1, axis=1)

print(inputArray)
print(arrDel)
arrDel = np.insert(arrDel, 1, new_col, axis=1)
print(arrDel)

ndArr = np.array([1,2,3,4], ndmin=6)
print(ndArr)

arrTwoDim = np.array([("x1", "x2"), ("x3", "x4")])
arrOneDim = np.array([3, 4, 6, 7])
print(arrTwoDim.shape)
print(arrOneDim.shape)

# PyChecker - Static Analysis tool -> helps find bugs in Python src code files and raises alerts for code issues and their complexity;
# Pylint - linting tool ->check for module's coding stds and supports diff plugins to enable custom features to meet the rept

# class Solution:
#     # @param A : integer
#     # @param B : integer
#     # @param C : integer
#     # @return a list of integers
# def solve(self, A, B, C):
#     print(A, B, C)
#     for i in range( C):
#         A, B = B - 2 * A, 2 * B + A
#     return A, B
#
# a, b = solve(2, 4, 5)
# print(a, b)

a = [7, 3, 8, 1, 4]
for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if a[i] < a[j]:
            a[i], a[j]=a[j],a[i]
print(a)
print(print("---Hello"))

print(2 ** 3 ** 2)
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
result = set1 & set2
print(result)
s = {1, 2, 3}
r = {2, 3, 4, 5}
t = {5, 6, 7}
u = s | r & t
print(u)

nums = [10, 20, 30, 40, 50]
print(nums[-3:-1])

r = np.array([1, 2, 3]) + np.array([[1], [2], [3]])
print(r)