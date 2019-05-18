def num_divisor_sum(num):
    sum = 1
    for i in range(2, num):
        if num % i == 0:
            sum += i
    if num != 1 and num == sum:
        print(num)


for num in range(1, 10001):
    num_divisor_sum(num)
