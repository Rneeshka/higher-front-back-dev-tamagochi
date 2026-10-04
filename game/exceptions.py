"""Модуль с исключениями."""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(Exception):
    """Ошибка, когда не хватает монет для покупки."""


class EmptyBag(Exception):
    """Ошибка, когда сумка пустая."""


class MedicineIsEmpty(Exception):
    """Ошибка, когда пытаемся применить использованное лекарство."""
