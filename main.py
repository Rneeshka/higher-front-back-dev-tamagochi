"""Точка входа в игру."""

import os

from game.clicker import RandomClicker
from game.exceptions import (
    EmptyBag,
    MedicineIsEmpty,
    NotEnoughMoney,
    TamagochiIsGone,
)
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi

MENU_ITEMS = [
    "1. Пойти на работу",
    "2. Купить еду",
    "3. Купить лекарство",
    "4. Покормить",
    "5. Вылечить",
    "6. Играть",
    "7. Отдых",
    "0. Выход",
]
MENU = '\n'.join(MENU_ITEMS)

STATUS = (
    '\nСтатус: голод {hunger}, здоровье {hp}, '
    'энергия {energy}, монет {coins}\n'
)


def ask_index(items: list) -> int | None:
    """
    Показывает список с номерами и спрашивает номер у игрока.

    :param items: список еды или лекарств
    :return: индекс в списке или None, если игрок нажал Enter
    """
    for number, item in enumerate(items, start=1):
        print(f'{number}. {item.name}')
    answer = input('Номер (Enter - по умолчанию): ')
    if not answer:
        return None
    return int(answer) - 1


def main() -> None:
    """Запускает игровой цикл."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = SimpleTamagochi()

    clicker = RandomClicker(10, 20)

    game = SimpleGame(
        tamagochi, clicker, all_food=all_food, all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")
        print(STATUS.format(**game.get_status()))

        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
        print(MENU)

        try:
            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                case "2":
                    game.buy_food(ask_index(all_food))
                    output = "Еда куплена"
                case "3":
                    game.buy_medicine(ask_index(all_medicine))
                    output = "Лекарство куплено"
                case "4":
                    game.feed_tamagochi(ask_index(game.food))
                    output = "Тамагочи поел"
                case "5":
                    game.heal_tamagochi()
                    output = "Тамагочи вылечился"
                case "6":
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case "7":
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case "0":
                    break
                case _:
                    output = "Неверная команда"
        except (
            NotEnoughMoney,
            EmptyBag,
            MedicineIsEmpty,
            ValueError,
            IndexError,
        ) as error:
            output = str(error)
        except TamagochiIsGone as error:
            print(error)
            break

        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()
