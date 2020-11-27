Суть проекта — отследить влияние условий жизни учащихся в возрасте от 15 до 22 лет на их успеваемость по математике, 
чтобы на ранней стадии выявлять студентов, находящихся в группе риска.

Описание датасета

1 school — аббревиатура школы, в которой учится ученик

2 sex — пол ученика ('F' - женский, 'M' - мужской)

3 age — возраст ученика (от 15 до 22)

4 address — тип адреса ученика ('U' - городской, 'R' - за городом)

5 famsize — размер семьи('LE3' <= 3, 'GT3' >3)

6 Pstatus — статус совместного жилья родителей ('T' - живут вместе 'A' - раздельно)

7 Medu — образование матери (0 - нет, 1 - 4 класса, 2 - 5-9 классы, 3 - среднее специальное или 11 классов, 4 - высшее)

8 Fedu — образование отца (0 - нет, 1 - 4 класса, 2 - 5-9 классы, 3 - среднее специальное или 11 классов, 4 - высшее)

9 Mjob — работа матери ('teacher' - учитель, 'health' - сфера здравоохранения, 'services' - гос служба, 'at_home' - не работает, 'other' - другое)

10 Fjob — работа отца ('teacher' - учитель, 'health' - сфера здравоохранения, 'services' - гос служба, 'at_home' - не работает, 'other' - другое)

11 reason — причина выбора школы ('home' - близость к дому, 'reputation' - репутация школы, 'course' - образовательная программа, 'other' - другое)

12 guardian — опекун ('mother' - мать, 'father' - отец, 'other' - другое)

13 traveltime — время в пути до школы (1 - <15 мин., 2 - 15-30 мин., 3 - 30-60 мин., 4 - >60 мин.)

14 studytime — время на учёбу помимо школы в неделю (1 - <2 часов, 2 - 2-5 часов, 3 - 5-10 часов, 4 - >10 часов)

15 failures — количество внеучебных неудач (n, если 1<=n<=3, иначе 0)

16 schoolsup — дополнительная образовательная поддержка (yes или no)

17 famsup — семейная образовательная поддержка (yes или no)

18 paid — дополнительные платные занятия по математике (yes или no)

19 activities — дополнительные внеучебные занятия (yes или no)

20 nursery — посещал детский сад (yes или no)

21 higher — хочет получить высшее образование (yes или no)

22 internet — наличие интернета дома (yes или no)

23 romantic — в романтических отношениях (yes или no)

24 famrel — семейные отношения (от 1 - очень плохо до 5 - очень хорошо)

25 freetime — свободное время после школы (от 1 - очень мало до 5 - очень мого)

26 goout — проведение времени с друзьями (от 1 - очень мало до 5 - очень много)

27 health — текущее состояние здоровья (от 1 - очень плохо до 5 - очень хорошо)

28 absences — количество пропущенных занятий

29 score — баллы по госэкзамену по математике

Ячейка кода ниже загружает необходимые библиотеки Python и загрузить данные датасета. 
Последний столбец из этого набора данных будет нашей целевой величина (независимо от того, закончил ли студент или не закончил). 
Все остальные колонки-это характеристики о каждом студенте.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind
import os

pd.set_option('display.max_rows', 50)  # показывать больше строк
pd.set_option('display.max_columns', 50)  # показывать больше колонок

stud = pd.read_csv('stud_math.csv')

Убираем столбец не названый в описании датасета

stud.drop(['studytime, granular'], inplace=True, axis=1)

Приведем название колонок к одному виду

stud.columns = ['school', 'sex', 'age', 'address', 'famsize', 'pstatus', 'medu', 'fedu',
       'mjob', 'fjob', 'reason', 'guardian', 'traveltime', 'studytime',
       'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'famrel',
       'freetime', 'goout', 'health', 'absences', 'score']

stud.head()

Добавим функции для упрощения дальнейших расчетов

def chgNonenuniq(row):
    '''Заменяем NaN на None.
Подсчитываем количество уникальных значений'''
    if stud[row].dtype != object:
        stud[row].hist()
        display(pd.DataFrame(stud[row].value_counts()))
        print("Уникальных значений:", stud[row].nunique())
        stud.loc[:, [row]].info()
    else:
        stud[row] = stud[row].astype(str).apply(lambda x: None if x.strip(
        ) == '' else None if x == 'nan' or x == 'NaN' else x)
        display(pd.DataFrame(stud[row].value_counts()))
        print("Уникальных значений:", stud[row].nunique())
        stud.loc[:, [row]].info()

def outliers(row):
    '''Находим границы выбросов и значения лежащий в межквартильном размахе    '''

    median = stud[row].median()
    perc25 = stud[row].quantile(0.25)
    perc75 = stud[row].quantile(0.75)
    IQR = perc75 - perc25
    print('25-й перцентиль: {},'.format(perc25), '75-й перцентиль: {},'.format(perc75),
          "IQR: {}, ".format(IQR), "Границы выбросов: [{f}, {l}].".format(f=perc25 - 1.5*IQR, l=perc75 + 1.5*IQR))
    stud[row].loc[stud[row].between(perc25 - 1.5*IQR, perc75 + 1.5*IQR)].hist(bins=16, range=(stud[row].min()-10, stud[row].max()+10),
                                                                              label='IQR')
    plt.legend()

Рассмотрим каждый признак

Для начала приведем пустые значения предсказываемой величины к нулю, для дальнейших расчетов корреляционного анализа.
В расчет принимаем что значение 0 означает что человек не пришел на экзамен и не получил баллы.

stud.score = stud.score.apply(lambda x: 0 if pd.isnull(x) else x)

chgNonenuniq(row='school')

chgNonenuniq(row='sex')

chgNonenuniq(row='age')
stud['age'].describe()

По графику видно, что основное количество учеников находится в возрасте от 15 до 19 лет, проверим данную категорию на наличие выбросов.

outliers(row='age')

Технически ученика 22 лет можно считать исключением из датесета по данной категории,
но в условии сказано, что 22 входит в диапозон учащихся в возрасте от 15 до 22 лет, 
следовательно 22 мы не выбрасываем из данного датасета.

Пустые значение приведем к значению обозначающему отсутвие адреса, поскольку удаление строк с отсутвующими данными 
или замена наиболее популярным значением может сильно сказаться на точности анализа.

stud.address = stud.address.apply(lambda x: "noadress" if pd.isnull(x) else x)

chgNonenuniq(row='address')

stud.address.sort_values()

stud.famsize = stud.famsize.apply(lambda x: "nofamsize" if pd.isnull(x) else x)

chgNonenuniq(row='famsize')

stud.pstatus = stud.pstatus.apply(lambda x: "nopstatus" if pd.isnull(x) else x)

chgNonenuniq(row='pstatus')

chgNonenuniq(row='medu')
stud['medu'].describe()

outliers(row='medu')

В данной категории выбросов нет, поскольку минимальные и максимальные значения внутри границ выбросов.

Заменим пустые значения на медиану.

stud.medu = stud.medu.apply(lambda x: stud.medu.median() if pd.isnull(x) else x)

chgNonenuniq(row='fedu')
stud['fedu'].describe()

Заменим пустые значения на медиану.

stud.fedu = stud.fedu.apply(lambda x: stud.fedu.median() if pd.isnull(x) else x)

Видно что присутствует всего одно значение отличающееся от остальных. Допустим, что такое большое значение является опечаткой 
и на самом деле соответсвует последнему ответу.

stud.loc[(stud['fedu'] == stud.fedu.max()),'fedu'] = 4
stud.fedu.head(12)

chgNonenuniq(row='fedu')

chgNonenuniq(row='mjob')

Пустые значение приравняем к значению 'other'

stud.mjob = stud.mjob.apply(lambda x: 'other' if pd.isnull(x) else x)

chgNonenuniq(row='fjob')

Пустые значение приравняем к значению 'other'

stud.fjob = stud.fjob.apply(lambda x: 'other' if pd.isnull(x) else x)

chgNonenuniq(row='reason')

Пустые значение приравняем к значению 'other'

stud.reason = stud.reason.apply(lambda x: 'other' if pd.isnull(x) else x)

chgNonenuniq(row='guardian')

chgNonenuniq(row='traveltime')
stud['traveltime'].describe()

Заменим пустые значения на медиану

stud.traveltime = stud.traveltime.apply(lambda x: stud.traveltime.median() if pd.isnull(x) else x)

outliers(row='traveltime')

stud.traveltime.sort_values()

Мы видим что значение "4" для данного показетеля является выбросом, но устранять его из основного датасета 
не будем поскольку данный признак является категориальным и значимым.

chgNonenuniq(row='studytime')
stud['studytime'].describe()

Заменим пустые значения на медиану.

stud.studytime = stud.studytime.apply(lambda x: stud.studytime.median() if pd.isnull(x) else x)

outliers(row='studytime')

Мы видим что значение "4" для данного показетеля является выбросом, но устранять его из основного датасета 
не будем поскольку данный признак является категориальным и значимым.

chgNonenuniq(row='failures')
stud['failures'].describe()

outliers(row='failures')

Данный показатель является не очень точным, поскольку показывает количество внеучебных неудач либо от одного до трех, 
либо все остальное, включая большее количество неудач и меньшее.
Поскольку последние значения сильно преобладают, то и все остальные значения можно считать выбросом, 
но это будет не верно для нашего анализа.

Пустые значение приравниваем к 0, как к наиболее часто встречающемуся значению.

stud.failures = stud.failures.apply(lambda x: 0 if pd.isnull(x) else x)

chgNonenuniq(row='schoolsup')

Отсуствие упоминания о доп. образовании прировняем к отсутвию доп. образования.

stud.schoolsup = stud.schoolsup.apply(lambda x: "no" if pd.isnull(x) else x)

chgNonenuniq(row='famsup')

С этой категорией поступаем так же

stud.famsup = stud.famsup.apply(lambda x: "no" if pd.isnull(x) else x)

chgNonenuniq(row='paid')

stud.paid = stud.paid.apply(lambda x: "no" if pd.isnull(x) else x)

chgNonenuniq(row='activities')

Пустые значение приводим к значению обозначающему отсутвие, поскольку удаление строк с отсутвующими данными 
или замена наиболее популярным значением может сильно сказаться на точности анализа.

stud.activities = stud.activities.apply(lambda x: "noactivities" if pd.isnull(x) else x)

chgNonenuniq(row='nursery')

Поступаем по аналогии с предыдущим

stud.nursery = stud.nursery.apply(lambda x: "nonursery" if pd.isnull(x) else x)

chgNonenuniq(row='higher')

Отсуствие упоминания о желании получения высшего прировняем к отсутвию желания получения высшего.

stud.higher = stud.higher.apply(lambda x: "no" if pd.isnull(x) else x)

chgNonenuniq(row='internet')

Пустые значение приводим к значению обозначающему отсутвие, поскольку удаление строк с отсутвующими данными 
или замена наиболее популярным значением может сильно сказаться на точности анализа.

stud.internet = stud.internet.apply(lambda x: "nointernet" if pd.isnull(x) else x)

chgNonenuniq(row='romantic')


Отсуствие упоминания о романтических отношениях прировняем к отсутвию романтических отношенияй.

stud.romantic = stud.romantic.apply(lambda x: "no" if pd.isnull(x) else x)

chgNonenuniq(row='famrel')
stud['famrel'].describe()

outliers(row='famrel')

Предположим что значение -1 один является ошибкой и поменяем его на 1

stud.loc[(stud['famrel']==-1),'famrel'] = 1

Заменим пустые значения на медиану

stud.famrel = stud.famrel.apply(lambda x: stud.famrel.median() if pd.isnull(x) else x)

Как видно что все значения ниже 2.5, а именно 2 и 1, считаются выбросами, отбросим только 1

a = len(stud)
stud = stud.loc[stud['famrel']>=2]
print(f'{a - len(stud)} - количество устранненых выбросов')

chgNonenuniq(row='freetime')
stud['freetime'].describe()

outliers(row='freetime')

stud.freetime = stud.freetime.apply(lambda x: stud.freetime.median() if pd.isnull(x) else x)

Мы видим, что все значения меньше полутора являются выбросом, но по моему мнению количество значений достачное, чтобы их не считать выбросом.

chgNonenuniq(row='goout')
stud['goout'].describe()

outliers(row='goout')

stud.goout = stud.goout.apply(lambda x: stud.goout.median() if pd.isnull(x) else x)

Для данного показетелем все распределенно равномерно, выбросов -  нет.

chgNonenuniq(row="health")
stud['health'].describe()

outliers(row='health')

stud.health = stud.health.apply(lambda x: stud.health.median() if pd.isnull(x) else x)

Схожая ситуация с предыдущим показателем, все распределенно равномерно, выбросов -  нет.

chgNonenuniq(row="absences")
stud['absences'].describe()

outliers(row='absences')

stud.absences = stud.absences.apply(lambda x: stud.absences.median() if pd.isnull(x) else x)

Отбросим очевидно большие значения

a = len(stud)
stud = stud.loc[stud['absences']<=100]
print(f'{a - len(stud)} - количество устранненых выбросов')

Произведена первичная обработка данных
Найдены уникальные значения
Приступим к кореляционному анализу

stud

stud_filter=stud.drop(['school', 'sex', 'address', 'famsize', 'pstatus', 'medu', 'fedu',
       'mjob', 'fjob', 'reason', 'guardian', 'traveltime', 'studytime',
       'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout',
       'health'], axis=1)

stud_filter

sns.pairplot(stud_filter, kind = 'score')

Используем для наглядности матрицу корреляций:

stud_filter.corr()

Все переменные слабоскоррелированные

def get_boxplot(column):
    fig, ax = plt.subplots(figsize = (14, 4))
    sns.boxplot(x=column, y='score', 
                data=stud.loc[stud.loc[:, column].isin(stud.loc[:, column].value_counts().index[:10])],
               ax=ax)
    plt.xticks(rotation=45)
    ax.set_title('Boxplot for ' + column)
    plt.show()

for col in ['school', 'sex', 'address', 'famsize', 'pstatus', 'medu', 'fedu',
       'mjob', 'fjob', 'reason', 'guardian', 'traveltime', 'studytime',
       'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout',
       'health']:
    get_boxplot(col)

def get_stat_dif(column):
    cols = stud.loc[:, column].value_counts().index[:10]
    combinations_all = list(combinations(cols, 2))
    for comb in combinations_all:
        if ttest_ind(stud.loc[stud.loc[:, column] == comb[1], 'score'], 
                        stud.loc[stud.loc[:, column] == comb[0], 'score']).pvalue \
            <= 0.05/len(combinations_all): # Учли поправку Бонферони
            print('Найдены статистически значимые различия для колонки', column)
            break

Проверим, есть ли статистическая разница в распределении оценок по номинативным признакам, с помощью теста Стьюдента. Проверим нулевую гипотезу о том, что распределения баллов по госэкзамену по математике по различным параметрам неразличимы:

for col in ['school', 'sex', 'address', 'famsize', 'pstatus', 'medu', 'fedu',
       'mjob', 'fjob', 'reason', 'guardian', 'traveltime', 'studytime',
       'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout',
       'health']:
    get_stat_dif(col)

Оставим эти переменные в датасете для дальнейшего построения модели. Итак, в нашем случае важные переменные, которые, возможно, оказывают влияние на оценку, это: sex, medu, mjob, guardian, failures, schoolsup, romantic, goout.

stud_model = stud.loc[:, ['sex', 'medu', 'mjob', 'guardian', 'failures', 'schoolsup', "romantic", 'goout','score']]
stud_model.head()

Пройдемся по каждой из этих переменных:
    sex - пол имеет два значения и не имеет выбросов.
    medu - имеет 5 различных уникальных значений в зависимости от образования матери, в данной категории выбросов нет 
    mjob - имеет 5 различных уникальных значений в зависимости от работы матери, в данной категории выбросов нет 
    guardian - имеет 3 различных уникальных значения в зависимости от опекунства, в данной категории выбросов нет 
    failures - Как уже говорилось данный показатель является не очень точным, поскольку показывает количество внеучебных неудач либо от одного до трех,
    либо все остальное, включая большее количество неудач и меньшее.
    schoolsup - имеет 2 различных уникальных значения в зависимости от наличия дополнительной образовательной поддержки
    romantic - имеет 2 различных уникальных значения в зависимости от наличия  романтических отношенияй 
    goout - имеет 5 различных уникальных значений в зависимости  времени проводимого с друзьями

1. Какова была ваша роль в команде?
Делал самостоятельно

2. Какой частью своей работы вы остались особенно довольны?
На самом деле мне кажется, что модель оказалось не совсем верной и требует переработки 

3. Что не получилось сделать так, как хотелось? Над чем ещё стоит поработать?
Не получилось сделать красивую структурированную систему, стоит поработь над графиками и их построением

4. Что интересного и полезного вы узнали в этом модуле?
На мой взгляд, этот модуль условно является подготовкой к работе Data Scientist'a, а именно подоготовительной частью проекта

5. Что является вашим главным результатом при прохождении этого проекта?
Про результат сложно сказать поскольку я не уверен в правильности проекта

6. Какие навыки вы уже можете применить в текущей деятельности?
Пока что никакие, если подразумевается текущая рабочая деятельность, если в плане учебней деятельности,
то почти все навыки из предидущих модулей

7. Планируете ли вы дополнительно изучать материалы по теме проекта?
Возможно