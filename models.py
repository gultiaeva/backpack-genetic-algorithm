import random


class BackpackFactory:
    """
    Завод по укладыванию вещей в рюкзаки.

    :param items: Предметы
    :param max_volume: Максимальный объем рюкзака
    :param alpha: Количество лучших особей из предыдущего поколения,
        которые пойдут в следующее
    :param max_generations: Максимальное количество поколений
    :param max_specimen: Максимальное количество особей в поколении
    :param crossover_type: Тип кроссовера. 
        Random -- случайный выбор 
        Avg -- среднее между родителями
    :param crossover_probability: Вероятность кроссовера
    :param mutation_probability: Вероятность мутации
    :param epsilon: Точность функции приспособленности
    """
    def __init__(self,  
                 items,
                 max_volume=50, 
                 alpha=2, 
                 max_generations=5000, 
                 max_specimen=100, 
                 crossover_type='random',
                 crossover_probability=.85, 
                 mutation_probability=.5,
                 epsilon=.01):

        assert crossover_type in ('random', 'avg'), 'Invalid crossover type'

        self.items = items  # List of Item
        self.types_count = len(items)
        self.max_volume = max_volume
        self.alpha = alpha
        self.max_generations = max_generations
        self.max_specimen = max_specimen
        if crossover_type == 'rand':
            self.crossover = self.rand_crossover
        else:
            self.crossover = self.avg_crossover
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.epsilon = epsilon

    def create_rand_backpack(self):
        """Создает случайную допустимую особь."""

        backpack_volume = 0
        available_items = self.items
        item_counts = [0] * self.types_count  # изначально особь пустая
        while len(available_items) != 0:
            available_items = list(filter(lambda x: x.volume <= self.max_volume - backpack_volume,
                                          available_items))
            if len(available_items) == 0:
                break
            item = random.choice(available_items)  # выбираем случайный предмет

            # выбираем случайное количество предмета
            if len(available_items) == 1:
                item_count = int((self.max_volume - backpack_volume) / item.volume)
            else:
                item_count = random.randint(1, (self.max_volume - backpack_volume) // item.volume)

            item_counts[item.number] += item_count  # добавляем количества предмета на соответствующую позицию
            backpack_volume += item_count * item.volume  # увеличиваем текущую вместимость особи

        return Backpack(self.items, item_counts)

    def create_start_generation(self):
        """Создает стартовое поколение."""

        backpacks = [self.create_rand_backpack() for _ in range(self.max_specimen)]
        return Generation(backpacks)

    def rand_crossover(self, parent_1, parent_2):
        """Проводит случайный кроссовер (случайный выбор частей родителей)."""

        for _ in range(10):  # TODO: чекнуть кол-во попыток

            crossover_counts = [random.choice([par1_arg, par2_arg]) 
                                for par1_arg, par2_arg in zip(parent_1.item_counts, 
                                                              parent_2.item_counts)]
            backpack = Backpack(self.items, crossover_counts)
            if backpack.volume <= self.max_volume:
                return backpack

        return parent_1 if parent_1.cost > parent_2.cost else parent_2

    def avg_crossover(self, parent_1, parent_2):
        """Проводит avg кроссовер (Среднее частей родителей)."""
        for _ in range(10):  # TODO: чекнуть кол-во попыток
            crossover_counts = [(par1_arg + par2_arg) // 2 
                                for par1_arg, par2_arg in zip(parent_1.item_counts,
                                                              parent_2.item_counts)]
            backpack = Backpack(self.items, crossover_counts)
            if backpack.volume <= self.max_volume:
                return backpack
            print('here')
        return parent_1 if parent_1.cost > parent_2.cost else parent_2

    def create_new_generation(self, generation):
        """Создает новое поколение особей."""
        new_backpacks = []

        for _ in range(2 * self.max_specimen): 
            if random.random() <= self.mutation_probability:
                mutated_backpack = self.create_rand_backpack()
                new_backpacks.append(mutated_backpack)
                continue

            parent_1, parent_2 = random.sample(list(generation), k=2)

            if random.random() <= self.crossover_probability:
                crossovered_backpack = self.crossover(parent_1, parent_2)
                new_backpacks.append(crossovered_backpack)
                continue

            new_backpacks.append(parent_1 if parent_1.cost > parent_2.cost else parent_2)

        alpha_best = sorted(generation, key=lambda x: x.cost, reverse=True)[:self.alpha]
        new_backpacks.extend(alpha_best)
        new_backpacks = sorted(new_backpacks, key=lambda x: x.cost, reverse=True)

        return Generation(new_backpacks[0:self.max_specimen])

    def evolve(self):
        """Запускает процесс эволюции."""

        generation = self.create_start_generation()
        print('Поколение 0')
        print(generation)
        max_cost = generation.cost

        for i in range(1, self.max_generations+1):
            new_generation = self.create_new_generation(generation)
            if i % 10 == 0:
                print(f"Приспособленность поколения {i}: {generation.cost:.4f}")
            if abs(new_generation.cost - max_cost) < self.epsilon:
                print(f"Поколение {i} -- выход")
                break

            generation = new_generation
        print()

        print(f"Поколение {i}: ")
        print(generation)


class Generation:
    """
    Поколение особей.

    :param backpacks: Список особей
    """
    def __init__(self, backpacks):
        self.backpacks = backpacks

    @property
    def cost(self):
        return sum(item.cost for item in self) / len(self)

    def __len__(self):
        return len(self.backpacks)

    def __iter__(self):
        return iter(self.backpacks)

    def __repr__(self):
        objs = '\n'.join(backpack.__repr__() for backpack in self)
        cost = self.cost
        return f'''Объекты: {objs}\nПриспособленность поколения: {cost}'''

    
class Backpack:
    """
    Рюкзак.

    :param items: Список всех вещей
    :param item_counts: Список из количеств каждой вещи, лежащих в рюкзаке 
    """
    
    def __init__(self, items, item_counts):
        self.items = items
        self.item_counts = item_counts

    @property
    def cost(self):
        return sum([cnt * item.cost for cnt, item in zip(self.item_counts, self.items)])

    @property
    def volume(self):
        return sum([cnt * item.volume for cnt, item in zip(self.item_counts, self.items)])

    def __repr__(self):
        return "[Стоимость {}; Предметы: {}]".format(self.cost, self.item_counts)


class Item:
    """
    Вещь.
    
    :param number: Порядковый номер вещи
    :param volume: Объем вещи
    :param cost: Стоимость вещи
    """
    def __init__(self, number: int, volume: int, cost: int):
        self.number = number
        self.volume = volume
        self.cost = cost

    def __repr__(self):
        return "[Вес: {}. Стоимость: {}]".format(self.volume, self.cost)
