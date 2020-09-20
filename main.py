import random

from models import BackpackFactory, Item


types_count = int(input("Задайте количество различных типов предметов: "))

print("Выберите способ задания начальных условий:")
print("1. Ручной")
print("2. Случайный")

case = input()

if case == "1":
    max_volume = int(input("Введите объем рюкзака: "))
    alpha = int(input("Введите количество лучших особей из предыдущего поколения, которые будут в следующем: "))
    max_generations = int(input("Введите максимальное количество поколений: "))
    max_specimen = int(input("Введите максимальное количество особей в поколении: "))
    crossover_type = input("Введите тип кроссовера (random, avg): ")
    crossover_probability = float(input("Введите вероятность кроссовера: "))
    mutation_probability = float(input("Введите вероятность мутации: "))
    epsilon = float(input("Введите точность функции приспособленности: "))

    items = [Item(i, random.randint(1, 20), random.randint(1, 20)) for i in range(types_count)]
    backpack = BackpackFactory(items, 
                               max_volume, 
                               alpha, 
                               max_generations, 
                               max_specimen, 
                               crossover_type, 
                               crossover_probability, 
                               mutation_probability, 
                               epsilon)

elif case == "2":
    items = [Item(i, random.randint(1, 20), random.randint(1, 20)) for i in range(types_count)]
    backpack = BackpackFactory(items)

else:
    exit(1)

print("Список предметов: ", end='')
for item in backpack.items:
    print(item)
print()

print("Максимальная вместимость: ", backpack.max_volume)
print("Количество лучших особей из предыдущего поколения: ", backpack.alpha)
print("Точность функции приспособленности: ", backpack.epsilon)
print("Максимальное количество поколений: ", backpack.max_generations)
print("Максимальное количество особей в поколении: ", backpack.max_specimen)
print("Вероятность кроссовера: ", backpack.crossover_probability, sep='')
print("Вероятность мутации: ", backpack.mutation_probability, sep='')

backpack.evolve()
