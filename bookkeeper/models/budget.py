"""
Class for budget representation.
"""

from dataclasses import dataclass


@dataclass
class Budget:
    """Budget for one day.
    """
    amount: float = 0.0
    pk: int = 0
