"""Модуль с интерфейсом и реализациями класса тамагочи."""

from abc import ABC, abstractmethod

from .exceptions import MedicineIsEmpty
from .models import Food, Medicine

START_HP = 100
START_HUNGER = 0
START_ENERGY = 100
MIN_STAT = 0
MAX_STAT = 100
ENERGY_CONSUM = 10
ENERGY_PLAY = 15
PLAY_HUNGER = 10
REST_ENERGY = 30
SICK_REST_ENERGY = 10
TICK_HUNGER = 5
TICK_ENERGY = 5
SICK_HUNGER_LIMIT = 70
SICK_ENERGY_LIMIT = 20
SICK_HP_LOSS = 10


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи.

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи.

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи.

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.

        Должен использоваться после каждого взаимодействия с тамагочи.
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Питомец Тамагочи."""

    def __init__(self) -> None:
        """Создает питомца со стартовыми значениями."""
        self._hp = START_HP
        self._hunger = START_HUNGER
        self._energy = START_ENERGY
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """
        Показывает состояние тамагочи: голод, здоровье и энергию.

        :return: словарь с состояниями тамагочи: голод, здоровье и энергия
        """
        return {'hunger': self._hunger, 'hp': self._hp, 'energy': self._energy}

    def is_alive(self) -> bool:
        """
        Показывает жив ли тамагочи.

        :return: True если жив, иначе False
        """
        return self._hp > MIN_STAT

    def is_sick(self) -> bool:
        """
        Показывает болен ли тамагочи.

        :return: True если тамагочи болеет, иначе False
        """
        return self._sick

    def feed(self, food: Food) -> None:
        """
        Кормит тамагочи: снижает голод и тратит энергию.

        :param food: объект еды для кормления
        """
        self._hunger = max(MIN_STAT, self._hunger - food.satiety)
        self._energy = max(MIN_STAT, self._energy - ENERGY_CONSUM)

    def play(self) -> None:
        """Тамагочи играет: повышает голод, уменьшает энергию."""
        self._hunger = min(MAX_STAT, self._hunger + PLAY_HUNGER)
        self._energy = max(MIN_STAT, self._energy - ENERGY_PLAY)

    def rest(self) -> None:
        """Отдых: восстанавливает энергию, при болезни слабее."""
        if self._sick:
            self._energy = min(MAX_STAT, self._energy + SICK_REST_ENERGY)
        else:
            self._energy = min(MAX_STAT, self._energy + REST_ENERGY)

    def heal(self, medicine: Medicine) -> None:
        """
        Лечит тамагочи: восстанавливает здоровье и снимает болезнь.

        :param medicine: лекарство для лечения
        :raises MedicineIsEmpty: если лекарство уже закончилось
        """
        if medicine.is_empty():
            raise MedicineIsEmpty(f"{medicine.name} закончилось")
        self._hp = min(MAX_STAT, self._hp + medicine.heal_hp)
        self._sick = False
        medicine.uses += 1

    def update(self) -> None:
        """Обновляет состояние после хода: голод, энергию и болезнь."""
        self._hunger = min(MAX_STAT, self._hunger + TICK_HUNGER)
        self._energy = max(MIN_STAT, self._energy - TICK_ENERGY)
        if (
            self._hunger > SICK_HUNGER_LIMIT
            or self._energy < SICK_ENERGY_LIMIT
        ):
            self._sick = True
        if self._sick:
            self._hp = max(MIN_STAT, self._hp - SICK_HP_LOSS)
