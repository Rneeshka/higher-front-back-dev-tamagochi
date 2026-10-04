"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from copy import copy
from typing import Any

from .clicker import AbstractClicker
from .exceptions import (
    EmptyBag,
    NotEnoughMoney,
    TamagochiIsGone,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ):
        """
        Абстрактный метод инициализации класса игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа".

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self, index: int | None = None) -> None:
        """
        Абстрактный метод для покупки еды.

        :param index: номер еды в магазине, по умолчанию самая дешевая
        """
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self, index: int | None = None) -> None:
        """
        Абстрактный метод для покупки лекарства.

        :param index: номер лекарства в магазине, по умолчанию самое дешевое
        """
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self, index: int | None = None) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        :param index: номер еды в сумке, по умолчанию последняя
        """
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи.

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой.

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами.

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Игра тамагочи-кликер."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Метод инициализации класса игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        self.tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._coins = 0
        self._bag_food = []
        self._bag_medicine = []

    def _next_turn(self) -> None:
        """
        Проверка состояния Тамагочи, проверяет жив ли он.

        :raises TamagochiIsGone: если тамагочи умер
        """
        self.tamagochi.update()
        if not self.tamagochi.is_alive():
            raise TamagochiIsGone("Тамагочи умер. Игра окончена")

    @property
    def food(self) -> list[Food]:
        """
        Свойство для доступа к сумке с едой.

        :return: список с имеющимися (купленными) объектами еды
        """
        return self._bag_food

    @property
    def medicine(self) -> list[Medicine]:
        """
        Свойство для доступа к сумке с лекарствами.

        :return: список с имеющимися (купленными) объектами лекарств
        """
        return self._bag_medicine

    def get_status(self) -> dict[str, Any]:
        """
        Метод для получения статуса (всех характеристик) тамагочи.

        :return: словарь со всеми характеристиками тамагочи
        """
        return {**self.tamagochi.status, 'coins': self._coins}

    def work(self) -> int:
        """
        Отправляет на работу: кликер приносит монеты.

        :raises TamagochiIsGone: если тамагочи умер
        :return: количество заработанных монет
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._next_turn()
        return income

    def buy_food(self, index: int | None = None) -> None:
        """
        Покупает еду из магазина.

        :param index: номер еды в магазине, по умолчанию самая дешевая
        :raises NotEnoughMoney: если не хватает монет
        """
        if index is None:
            food = min(self._all_food, key=lambda item: item.price)
        else:
            food = self._all_food[index]
        if food.price > self._coins:
            raise NotEnoughMoney(
                f'Не хватает монет на {food.name}: нужно {food.price}'
            )
        self._coins -= food.price
        self._bag_food.append(food)

    def buy_medicine(self, index: int | None = None) -> None:
        """
        Покупает лекарства из аптеки.

        :param index: номер лекарства в магазине, по умолчанию самое дешевое
        :raises NotEnoughMoney: если не хватает монет
        """
        if index is None:
            medicine = min(self._all_medicine, key=lambda item: item.price)
        else:
            medicine = self._all_medicine[index]
        if medicine.price > self._coins:
            raise NotEnoughMoney(
                f'Не хватает монет на {medicine.name}: нужно {medicine.price}'
            )
        self._coins -= medicine.price
        self._bag_medicine.append(copy(medicine))

    def feed_tamagochi(self, index: int | None = None) -> None:
        """
        Тамагочи ест.

        :param index: номер еды в сумке, по умолчанию последняя
        :raises EmptyBag: появляется, если сумка с едой пустая
        """
        if not self._bag_food:
            raise EmptyBag("Сумка пустая, еды нет")
        if index is None:
            meal = self._bag_food.pop(-1)
        else:
            meal = self._bag_food.pop(index)
        self.tamagochi.feed(meal)
        self._next_turn()

    def heal_tamagochi(self) -> None:
        """
        Тамагочи лечится.

        :raises EmptyBag: появляется, если сумка с лекарствами пустая
        :raises MedicineIsEmpty: появляется, когда лекарство уже использовано
        """
        if not self._bag_medicine:
            raise EmptyBag("Сумка пустая, лекарств нет")
        healing = self._bag_medicine[-1]
        self.tamagochi.heal(healing)
        if healing.is_empty():
            self._bag_medicine.pop(-1)
        self._next_turn()

    def rest_tamagochi(self) -> None:
        """Тамагочи отдыхает."""
        self.tamagochi.rest()
        self._next_turn()

    def play_with_tamagochi(self) -> None:
        """Тамагочи играет."""
        self.tamagochi.play()
        self._next_turn()
