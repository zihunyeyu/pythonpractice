def how_can_i_buy100chicken():
    for a in range(int(100/5)):
        for b in range(int(100/3)):
            for c in range(100*3):
                if a*5 + b*3 + c/3 == 100 and a + b + c == 100:
                    print('公鸡:', a, '母鸡:', b, '小鸡:', c)


how_can_i_buy100chicken()
