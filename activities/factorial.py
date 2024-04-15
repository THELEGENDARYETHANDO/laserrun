t = int(input("num"))

def factorial(x):
    num = 1
    while x >= 1:
        num *= x
        x -= 1
    return num

print(factorial(t))