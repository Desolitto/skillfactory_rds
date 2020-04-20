# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:56:03 2020

@author: diika
"""


import numpy as np
count = 0                            # счетчик попыток
number = 5#np.random.randint(1,101)    # загадали число
print ("Загадано число от 1 до 100")


for count in range(1,101):         # более компактный вариант счетчика
    count = 1
    predict = int((len(range(1,101))/2))
    predictm = int((len(range(1,101))/2)) + int((len(range(1,101))/4))
    predictl = int((len(range(1,101))/2)) - int((len(range(1,101))/4))
    while number != predict:
        count+=1
        if number > predict:
            while number > predict:
                if number > predictm: 
                    predictm += 1
                    predict = predictm
                elif number == predictm:
                    predict = predictm
                elif number < predictm:
                    predict += 1
        elif number < predict:
            while number < predict:
                if number > predictl: 
                    predictl += 1
                    predict = predictm
                elif number == predictl:
                    predict = predictm
                elif number < predictl:
                    predict -= 1
    break
    #predict = np.random.randint(1,101) # предполагаемое число
    #if number == predict: break    # выход из цикла, если угадали
    #elif number > predict: print (f"Угадываемое число больше {predict} ")
    #elif number < predict: print (f"Угадываемое число меньше {predict} ")
        
print (f"Вы угадали число {number} за {count} попыток.")