# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 18:00:49 2020

@author: diika
"""



import numpy as np
count = 0                            # счетчик попыток
number = np.random.randint(1,101)    # загадали число
a = 1
b = 100
predict = 0
print ("Загадано число от 1 до 100")
while number != predict:
    predict = (a + b) // 2
    count += 1
    if predict == number:
        print(f"Вы угадали число {number} за {count} попыток.")
    elif predict < number:
        b = predict - 1
    elif predict > number:
        a = predict + 1
print(f"Вы угадали число {number} за {count} попыток.")