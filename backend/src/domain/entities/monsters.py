from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Monster:
    id: str
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
    loot_table_ids: List[str]

    def is_alive(self) -> bool:
        return self.hp_current > 0

    def take_damage(self, amount: int) -> int:
        " Receives reduced damage by monster defense. Returns the real damage taken "

        # reduce damage by defense, but the minimum damage is equal to 1 if the hit connects
        actual_damage = max(1, amount - self.defense)

        self.hp_current -= actual_damage
        if self.hp_current < 0:
            self.hp_current = 0

        return actual_damage

