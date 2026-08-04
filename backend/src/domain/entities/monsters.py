from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4
from src.domain.entities.monster_loots import LootDrop

@dataclass(kw_only=True)
class Monster:
    id: UUID = field(default_factory=uuid4)
    name: str
    description: str
    level: int

    # Combat attributes
    hp_current: int
    hp_max: int
    attack_power: int
    defense: int

    # Kill rewards
    xp_reward: int
    gold_reward: int

    # dropped loot table ids
    loot_table_ids: List[LootDrop] = field(default_factory=list)

    def __post_init__(self):
        # spawn validation
        if self.hp_max <= 0:
            raise ValueError(f"The monster {self.name} must have max hp greater than 0.")

        if self.hp_current < 0 or self.hp_current > self.hp_max:
            raise ValueError("Current HP invalid for the monster.")

    def is_alive(self) -> bool:
        return self.hp_current > 0

    def take_damage(self, amount: int) -> int:
        """
        Receives reduced damage by monster defense. Returns the real damage taken.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        # reduce damage by defense, but the minimum damage is equal to 1 if the hit connects
        actual_damage = max(1, amount - self.defense)

        self.hp_current -= actual_damage
        if self.hp_current < 0:
            self.hp_current = 0

        return actual_damage

