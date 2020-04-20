import numpy as np
number = np.random.randint(1,101)    # загадали число
print ("Загадано число от 1 до 100")

def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)

def game_core_v3(number):
    '''Сначала устанавливаем цикл нахождения середины диапазона поиска,
       путем нахождения целой части среднего арифметического границ диапазона,
       а потом уменьшаем его верхнюю границу или увеличиваем его нижнюю границу в зависимости от того, больше оно или меньше нужного.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 0                         # счетчик попыток
    predict = 0
    a = 1                             # нижняя граница поиска числа
    b = 100                           # верхняя граница поиска числа 
    while number != predict:
        predict = (a + b) // 2     
        count += 1
        if predict == number:
            return(count) # выход из цикла, если угадали
        elif predict > number:
            b = predict - 1
        elif predict < number:
            a = predict + 1

# Проверяем
score_game(game_core_v3)