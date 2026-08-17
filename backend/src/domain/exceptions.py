from uuid import UUID

from src.domain.enums.character_class import CharacterClass
from src.domain.enums.equipment_slot import EquipmentSlot

class DomainError(Exception):
    """Base error for all domain rules."""

class LevelRequirementError(DomainError):
    def __init__(self, required: int, current: int) -> None:
        self.required = required
        self.current = current
        super().__init__(f"Level {current} is not enough. Item requires level {required}.")

class ClassRestrictionError(DomainError):
    def __init__(self, required: CharacterClass, current: CharacterClass) -> None:
        self.required = required
        self.current = current
        super().__init__(f"Class '{current}' cannot use this item. Required class: '{required}'.")


class InventoryError(DomainError):
    """Base error for inventory rules."""

class InventoryFullError(InventoryError):
    pass

class ItemNotFoundError(InventoryError):
    def __init__(self, item_id: UUID) -> None:
        self.item_id = item_id
        super().__init__(f"Item '{item_id}' is not in the inventory.")

class ItemNotEquippableError(InventoryError):
     def __init__(self, item_id: UUID) -> None:
        self.item_id = item_id
        super().__init__(f"Item '{item_id}' cannot be equipped.")

class ItemAlreadyEquippedError(InventoryError):
     def __init__(self, item_id: UUID) -> None:
        self.item_id = item_id
        super().__init__(f"Item '{item_id}' is already equipped.")

class ItemNotEquippedError(InventoryError):
     def __init__(self, slot: EquipmentSlot) -> None:
        self.slot = slot
        super().__init__(f"There is no item equipped in the '{slot}' slot.")