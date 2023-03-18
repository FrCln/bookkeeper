"""
Модель бюджета для расходов
"""
from dataclasses import dataclass


@dataclass
class Budget:
    """
    Бюджет, хранит сумму (total),
    рассчитанную на период времени (period),
    а также сумму (spent), потраченную за этот период.
    """
    total: int
    period: str
    spent: int = 0
    pk: int = 0

    def __post_init__(self) -> None:
        if self.period not in ["day", "month", "year"]:
            raise ValueError(f"Got unknown period: {self.period}")
