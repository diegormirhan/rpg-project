from dataclasses import dataclass
from typing import Optional

from src.domain.enums.character_class import CharacterClass

@dataclass
class Player:
    id: str
    user_id: str
    name: str
    character_class: CharacterClass
    level: int = 1
    xp: int = 0
    gold: int = 0
    hp_current: int = 100
    hp_max: int = 100
    mana_current: int = 50
    mana_max = int = 50

    def is_alive(self) -> bool:
        return self.hp_current > 0

    def take_damage(self, amount: int) -> None:
        self.hp_current -= amount
        if self.hp_current < 0:
            self.hp_current = 0

    def heal(self, amount: int) -> None:
        if not self.is_alive():
            return # Não pode curar se estiver morto

        self.hp_current += amount
        if self.hp_current > self.hp_max:
            self.hp_current = self.hp_max
        