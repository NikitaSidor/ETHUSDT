# Импортируем установленный модуль.
from prettytable import PrettyTable
import requests
import time
from os import system
from datetime import datetime 
#
price = []
# задаем начальную цену
start_price = None
end_price = float(0)
# задаем время проверки
start_time = None
# задаем начальное время
timeframe = 60.0*60
# задаем порог изменения цены (в процентах)
threshold = 1

# Создание таблицы
th = ["Время", "Цена", "Разница", "%", "Ставка"]
table = PrettyTable(th)

# делаем запрос к сайту биржи для получения цены фьючерса ETHUSDT возвращаем float
def get_ethusdt()->float:
    data = requests.get('https://fapi.binance.com/fapi/v1/ticker/24hr', params={'symbol': 'ETHUSDT'}).json()
    return float(data['lastPrice'])

# получаем данные по цене
def price_data()->None:
    global price
    if len(price)<6:
        price.append(get_ethusdt())
    else:
        price.pop(0)
        price.append(get_ethusdt())
# функция отслеживания
def start_surveillance(price)->bool:
    global timeframe, start_time, start_price, end_price
    if start_price == None:
        start_time = time.time()
        end_price = start_price = price
        return True
    elif time.time()-start_time >= timeframe:
        start_time = time.time()
        end_price = start_price
        start_price = price
        return True
    return False
# 
def price_color(price)->str:
    array = 'От старого к новому:'
    for i in range(len(price)):
        if(i+1 < len(price)):
            price_comparison = price[i]<price[i+1]
            price_equals = price[i+1]==price[i]
            # равно
            if price_equals:
                array += str(" \033[33m{}\033[0m".format(price[i+1]))
            # больше
            elif price_comparison:
                array += str(" \033[32m{}\033[0m".format(price[i+1]))
            # меньше
            else:
                array += str(" \033[31m{}\033[0m".format(price[i+1]))
    return array
def console_yellow(i)->str:
    return "\033[33m{}\033[0m".format(i)
def console_green(i)->str:
    return "\033[32m{}\033[0m".format(i)
def console_red(i)->str:
    return "\033[31m{}\033[0m".format(i)
def create_row_table()->list:
    global start_price, end_price
    date = datetime.now().time()
    price = start_price
    difference = f"{start_price-end_price:.4f}"
    persent = f"{(start_price*100/end_price-100):.4f}"
    bid = ''
    if start_price>end_price:
        difference = console_green(difference)
        persent = console_green(persent)
        bid = "Вырасла"
    elif start_price<end_price:
        difference = console_red(difference)
        persent = console_red(persent)
        bid = "Понизилась"
    return [date,price,difference,persent,bid]

while True:
    start = time.perf_counter()
    price_data()
    if start_surveillance(price[-1]):
        table.add_row(create_row_table())
    system('cls||clear')
    if start_price*100/end_price-100>=threshold and start_price*100/end_price-100<=-(threshold):
        print(console_green(f"\nВнимание ставка по таблице изменилась на {0}%".format(start_price*100/end_price-100)))
    print(table)  # Печатаем таблицу
    new_percent = price[-1]*100/start_price-100
    print("Изминение процента: {0}".format(new_percent))
    print(price_color(price))
    
    print(f"Время обновления: {time.perf_counter() - start}")
    if new_percent>=threshold and new_percent<=-(threshold):
        print(console_green(f"\nВнимание ставка изменилась на {0}%".format(new_percent)))
        print(price[-1])
