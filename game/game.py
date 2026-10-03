"""Модуль с интерфейсом и реализацией класса игры"""

import random
from abc import ABC, abstractmethod
from copy import copy
from typing import Any

from exceptions import NotEnoughMoney

from .clicker import AbstractClicker
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Игра тамагочи-кликер"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Метод инициализации класса игры

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

    @property
    def food(self) -> list[Food]:
        """
        Свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        return self._bag_food

    @property
    def medicine(self) -> list[Medicine]:
        """
        Свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        return self._bag_medicine

    def get_status(self) -> dict[str, Any]:
        """
        Метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        return {**self.tamagochi.status, 'coins': self._coins}

    def work(self) -> int:
        """
        Отправляет на работу: кликер приносит монеты

        :return: количество заработанных монет
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        return income

    def buy_food(self) -> None:
        """
        Покупает еду из магазина.

        :raises NotEnoughMoney: если не хватает монет
        """
        food = random.choice(self._all_food)
        if food.price > self._coins:
            raise NotEnoughMoney(
                f'Не хватает монет на {food.name}: нужно {food.price}'
            )
        else:
            self._coins -= food.price
            self._bag_food.append(food)

    def buy_medicine(self) -> None:
        """Покупает лекарства из аптеки.

        :raises NotEnoughMoney: если не хватает монет
        """
        medicine = random.choice(self._all_medicine)
        if medicine.price > self._coins:
            raise NotEnoughMoney(
                f'Не хватает монет на {medicine.name}: нужно {medicine.price}'
            )
        else:
            self._coins -= medicine.price
            self._bag_medicine.append(copy(medicine))

    def feed_tamagochi(self) -> None:
        """Тамагочи ест."""
        if not self._bag_food:
            return
        meal = self._bag_food.pop()
        self.tamagochi.feed(meal)
        self.tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Тамагочи лечится."""
        if not self._bag_medicine:
            return
        healing = self._bag_medicine[-1]
        self.tamagochi.heal(healing)
        if healing.is_empty():
            self._bag_medicine.remove(healing)
        self.tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Тамагочи отдыхает."""
        self.tamagochi.rest()
        self.tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Тамагочи играет."""
        self.tamagochi.play()
        self.tamagochi.update()
