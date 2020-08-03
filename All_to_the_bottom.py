import psycopg2 as psc
import collections
import numpy as np
from datetime import datetime
import time

#Подключение к базе
conn = psc.connect(
       database="all_to_the_bottom", 
       user="postgres", 
       password="qwerty", 
       host="127.0.0.1", 
       port="5432"
  )

def seconds(tm):

    y = list(map(int, tm.split(":")))
    sec = y[0]*3600 + y[1]*60 + y[2]

    return sec

def Question_1():

    curs = conn.cursor()

    curs.execute("SELECT \"IP\" FROM \"Requests\"")
    select_1 = curs.fetchall()
    request_ip = []
    i = 0
    while i < len(select_1):
        request_ip.append(select_1[i][0])
        i += 1


    count_1 = collections.Counter()
    for ip in request_ip:
        count_1[ip] += 1

    curs.execute("SELECT \"IP\",\"Country\" FROM \"Countries\"")
    select_2 = curs.fetchall()

    countries = []
    i = 0
    while i < len(select_2):
        countries.append(select_2[i][1])
        i += 1
    countries = set(countries)

    actions = []

    for c in countries:
        num = 0
        i = 0
        while i < len(select_2):
            if c == select_2[i][1]:
                num = num + count_1[select_2[i][0]]
            i += 1
        actions.append([num, c])

    actions.sort(reverse=True)
    i = 0
    while i < 6:
        print(actions[i][1], " = ", actions[i][0])
        i += 1

    return

def Question_2():

    curs = conn.cursor()

    curs.execute("SELECT \"IP\",\"Country\" FROM \"Countries\"")
    select_2 = curs.fetchall()
    curs.execute("SELECT \"IP\",\"Category\" FROM \"Requests\"")
    select_3 = curs.fetchall()

    q2_ip = []
    i = 0
    while i < len(select_3):
        if select_3[i][1] == "fresh_fish":
            q2_ip.append(select_3[i][0])
        i += 1

    q2_countries = []

    for ip in q2_ip:
        i = 0
        while i < len(select_2):
            if ip == select_2[i][0]:
                q2_countries.append(select_2[i][1])
            i += 1

    count_2 = collections.Counter()
    for ip in q2_countries:
        count_2[ip] += 1

    answer = list(count_2.most_common(7))
    i = 0
    while i < len(answer):
        print(answer[i][0], " = ", answer[i][1])
        i += 1

    return

def Question_3():

    curs = conn.cursor()

    curs.execute("SELECT \"Time\",\"Category\" FROM \"Requests\"")
    select_4 = curs.fetchall()
    time_list = []
    i = 0
    while i < len(select_4):
        if select_4[i][1] == "frozen_fish":
            time_list.append(seconds(str(select_4[i][0])))
        i += 1

    t = ["06:00:00", "12:00:00", "18:00:00", "24:00:00"]
    ts = []
    zones = [0, 0, 0, 0] # 00 - 06; 06 - 12; 12 - 18; 18 - 24;
    for i in t:
        ts.append(seconds(i))

    i = 0
    while i < len(time_list):
        if time_list[i] <= ts[0]:
            zones[0] += 1
        elif ts[0] < time_list[i] <= ts[1]:
            zones[1] += 1
        elif ts[1] < time_list[i] <= ts[2]:
            zones[2] += 1
        elif ts[2] < time_list[i] <= ts[3]:
            zones[3] += 1
        i += 1

    answer = zones.index(max(zones))
    if answer == 0:
        print("00:00 - 06:00")
    elif answer == 1:
        print("06:00 - 12:00")
    elif answer == 2:
        print("12:00 - 18:00")
    elif answer == 3:
        print("18:00 - 00:00")

    return

def Question_4():
    curs = conn.cursor()

    curs.execute("SELECT \"Time\", \"Category\" FROM \"Requests\"")
    select_5 = curs.fetchall()
    requests = []
    i = 1
    amount = 0
    while i < len(select_5):
        if seconds(str(select_5[i - 1][0])) <= seconds(str(select_5[i][0])):
            if select_5[i][1] == "None":
                amount += 1
        else:
            requests.append(amount)
            amount = 0
        i += 1

    print(max(requests))
    return

def Question_5():
    curs = conn.cursor()
    
    #id: 14 - 18
    curs.execute("SELECT \"Cart_id\",\"Success\" FROM \"Pays\"")
    select_6 = curs.fetchall()

    curs.execute("SELECT \"Cart_id\",\"Goods_id\" FROM \"Carts\"")
    select_7 = curs.fetchall()

    containing_carts = []
    i = 0
    while i < len(select_7):
        if 14 <= select_7[i][1] <= 18:
            j = 0
            while j < len(select_6):
                if select_7[i][0] == select_6[j][0]:
                    if select_6[j][1] == True:
                        containing_carts.append(select_7[i][0])
                j += 1
        i += 1

    containing_carts = set(containing_carts)

    zones_category = [0, 0, 0, 0, 0] #fresh_fish, frozen_fish, semi_manufactures, canned_food, caviar
    for id in containing_carts:
        i = 0
        while i < len(select_7):
            if id == select_7[i][0]:
                if 1 <= select_7[i][1] <= 7:
                    zones_category[0] += 1
                elif 8 <= select_7[i][1] <= 13:
                    zones_category[1] += 1
                elif 19 <= select_7[i][1] <= 21:
                    zones_category[3] += 1
                elif 21 <= select_7[i][1] <= 24:
                    zones_category[4] += 1
            i += 1

    answer = zones_category.index(max(zones_category))
    if answer == 0:
        print("fresh_fish")
    elif answer == 1:
        print("frozen_fish")
    elif answer == 2:
        print("canned_food")
    elif answer == 3:
        print("caviar")

    return

def Question_6():

    curs = conn.cursor()

    curs.execute("SELECT \"Success\" FROM \"Pays\"")
    select_8 = curs.fetchall()

    num = 0
    i = 0
    while i < len(select_8):
        if select_8[i][0] == False:
            num += 1
        i += 1
    print(num)

    return

def Question_7():

    curs = conn.cursor()

    curs.execute("SELECT \"Cart_id\",\"Success\" FROM \"Pays\"")
    select_9 = curs.fetchall()

    payed_carts = []
    i = 0
    while i < len(select_9):
        if select_9[i][1] == True:
            payed_carts.append(select_9[i][0])
        i += 1

    curs.execute("SELECT \"IP\",\"Cart_id\" FROM \"Carts\"")
    select_10 = curs.fetchall()
    select_10 = list(set(select_10))

    payed_ip = []
    i = 0
    while i < len(select_10):
        if (select_10[i][1] in payed_carts) == True:
            payed_ip.append(select_10[i][0])
        i += 1

    count_7 = collections.Counter()
    for ip in payed_ip:
        count_7[ip] += 1

    answer = list(count_7.most_common())
    i = 0
    num = 0
    while i >= 0:
        if answer[i][1] > 1:
            num += 1
        else:
            break;
        i += 1
    print(num)

    return

#Начало работы программы
print("Введите вопрос: ")
question = str(input()).lower()

if question == "посетители из какой страны совершают больше всего действий на сайте?":
    Question_1()
elif question == "посетители из какой страны чаще всего интересуются товарами из категории \"fresh_fish\"?":
    Question_2()
elif question == "в какое время суток чаще всего просматривают категорию \"frozen_fish\"?":
    Question_3()
elif question == "какое максимальное число запросов на сайт за астрономический час (c 00 минут 00 секунд до 59 минут 59 секунд)?":
    Question_4()
elif question == "товары из какой категории чаще всего покупают совместно с товаром из категории \"semi_manufactures\"?":
    Question_5()
elif question == "сколько брошенных (не оплаченных) корзин имеется?":
    Question_6()
elif question == "какое количество пользователей совершали повторные покупки?":
    Question_7()
else:
    print("На ваш вопрос ответ отсутствует. Пожалуйста, сформулируйте вопрос более точно.")

#Закрываем соединение с базой
close = input("Press enter to exit...")
conn.close()