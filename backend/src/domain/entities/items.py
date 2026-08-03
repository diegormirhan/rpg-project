from dataclasses import dataclass
from typing import Optional
from src.domain.enums.item_type import ItemType
from src.domain.enums.item_rarity import ItemRarity
from src.domain.enums.equipment_slot import EquipmentSlot

@dataclass
class Item:
    id: str
    name: str
    description: str
    item_type: ItemType
    rarity: ItemRarity

    # equipment values
    equipment_slot: Optional[EquipmentSlot] = None
    attack_bonus: int = 0
    defense_bonus: int = 0

    # consumable item
    heal_amount: int = 0

    # Market value
    gold_value: int = 0

    # Business rules
    def is_equippable(self) -> bool:
        equippable_types = [
            ItemType.WEAPON,
            ItemType.ARMOR,
            ItemType.HELMET,
            ItemType.BOOTS,
            ItemType.GLOVES,
            ItemType.SHIELD,
        ]
        return self.item_type in equippable_types

    def is_consumable(self) -> bool:
        return self.item_type == ItemType.CONSUMABLE