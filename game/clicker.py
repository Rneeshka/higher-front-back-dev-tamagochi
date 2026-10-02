"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class RandomClicker(AbstractClicker):
    """Кликер со случайным доходом за клик"""

    def __init__(self, min_income: int, max_income: int) -> None:
        """Инициализация кликера

        :param min_income: минимальный доход за клик
        :param max_income: максимальный доход за клик
        """
        self._min_income = min_income
        self._max_income = max_income
        self._last_income = 0

    def click(self) -> None:
        """Делает клик: определяет, сколько монет он принёс."""
        self._last_income = randint(self._min_income, self._max_income)

    @property
    def income_per_click(self) -> int:
        """
        Возвращает доход последнего клика.

        :return: количество монет за последний клик
        """
        return self._last_income
