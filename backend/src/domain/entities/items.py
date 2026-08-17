from dataclasses import dataclass, field
from typing import Optional, Dict
from uuid import UUID, uuid4

from src.domain.enums.item_type import ItemType
from src.domain.enums.item_rarity import ItemRarity
from src.domain.enums.equipment_slot import EquipmentSlot
from src.domain.enums.character_class import CharacterClass

_EQUIPMENT_SLOT_BY_TYPE: Dict[ItemType, EquipmentSlot] = {
    ItemType.WEAPON: EquipmentSlot.WEAPON,
    ItemType.ARMOR: EquipmentSlot.BODY,
    ItemType.HELMET: EquipmentSlot.HEAD,
    ItemType.BOOTS: EquipmentSlot.BOOTS,
    ItemType.GLOVES: EquipmentSlot.GLOVES,
    ItemType.SHIELD: EquipmentSlot.SHIELD,
}

@dataclass(kw_only=True)
class Item:
    id: UUID = field(default_factory=uuid4)
    name: str
    description: str
    item_type: ItemType
    rarity: ItemRarity

    # equipment values
    equipment_slot: Optional[EquipmentSlot] = None
    attack_bonus: int = 0
    defense_bonus: int = 0

    # restrictions
    class_restriction: Optional[CharacterClass] = None
    level_requirement: int = 1

    # stacking
    stackable: bool = False
    max_stack: int = 1

    # consumable item
    heal_amount: int = 0

    # Market value
    gold_value: int = 0

    # Business rules
    def is_equippable(self) -> bool:
        return self.item_type in _EQUIPMENT_SLOT_BY_TYPE

    def is_consumable(self) -> bool:
        return self.item_type == ItemType.CONSUMABLE

    def resolve_equipment_slot(self) -> Optional[EquipmentSlot]:
        """Returns the target slot. Explicit equipment slot wins over the type mapping."""
        if self.equipment_slot is not None:
            return self.equipment_slot
        return _EQUIPMENT_SLOT_BY_TYPE.get(self.item_type)