# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:56:03 2020

@author: diika
"""


import numpy as np
count = 0                            # счетчик попыток
number = np.random.randint(1,101)    # загадали число
print ("Загадано число от 1 до 100")


for count in range(1,101):         # более компактный вариант счетчика
    count = 1
    predict = int((len(range(1,101))/2))
    predictm = int((len(range(1,101))/2)) + int((len(range(1,101))/4))
    mredictl = int((len(range(1,101))/2)) - int((len(range(1,101))/4))
    while number != predict:
        count+=1
        if number > predict and number > predictm: 
            predictm += 1
            predict = predictm
        elif number > predict and number == predictm:
            predict == predictm
        elif number > predict and number < predictm:
            predictm -= 1
            predict = predictm
        elif number < predict: 
            predict -= 1
    break
    #predict = np.random.randint(1,101) # предполагаемое число
    #if number == predict: break    # выход из цикла, если угадали
    #elif number > predict: print (f"Угадываемое число больше {predict} ")
    #elif number < predict: print (f"Угадываемое число меньше {predict} ")
        
print (f"Вы угадали число {number} за {count} попыток.")