# 函数的递归
def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# for循环
def for_n(n):
    sum = 1
    if n == 1 or n == 2:
        return 1
    else:
        a = b = 1
        for i in range(2, n+1):
            a, b = b, a + b
        return a


# while循环
def while_n(n):
    a, b = 1, 1
    while a < n-1:
        a, b = b, a+b
    return a


n = int(input('输入项数：'))
print('迭代：', fibonacci(n), '\nfor循环：', for_n(n), '\nwhile循环', while_n(n))



