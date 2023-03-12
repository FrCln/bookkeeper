"""
Class for budget representation.
"""

from dataclasses import dataclass


@dataclass
class Budget:
    """Not quite sure what to do with it.
    """
    period: int
    category: int
    amount: int
    pk: int = 0
