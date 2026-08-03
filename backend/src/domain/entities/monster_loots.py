from dataclasses import dataclass
from typing import List

@dataclass
class LootDrop:
    "Represents an specific item that can be dropped and its chance of loot rarity"
    item_id: str
    drop_chance_percent: float
    min_quantity: int = 1
    max_quantity: int = 1

@dataclass
class MonsterLootTable:
    "Full rewards table from a monster"
    monster_id: str
    drops: List[LootDrop]

    #  Business rules
    def roll_loot(self, rng_roll_function) -> List[dict]:
        "Receives a rng function to decide which types of items will actually drop based on rarity type"
        dropped_items = []
        for loot in self.drops:
            roll = rng_roll_function
            if roll <= loot.drop_chance_percent:
                dropped_items.append({
                    "item_id": loot.item_id,
                    "min_qty": loot.min_quantity,
                    "max_qty": loot.max_quantity
                })
        return dropped_items