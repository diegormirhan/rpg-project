from dataclasses import dataclass, field
from typing import List, Dict, Optional
from uuid import UUID, uuid4

from src.domain.enums.equipment_slot import EquipmentSlot

@dataclass(kw_only=True)
class InventoryItem:
    """Represents the item and quantity that is inside the inventory."""
    id: UUID = field(default_factory=uuid4)
    quantity: int = 1


@dataclass(kw_only=True)
class Inventory:
    id: UUID = field(default_factory=uuid4)
    player_id: str
    max_slots: int = 30 # default inventory size

    # The list of items that the player has
    items: List[InventoryItem] = field(default_factory=list)

    # equipped items, one per equipment slot
    equipped: Dict[EquipmentSlot, InventoryItem] = field(default_factory=dict)

    def is_full(self) -> bool:
        # Checks if inventory is full
        return len(self.items) >= self.max_slots

    def available_slots(self) -> int:
        return max(0, self.max_slots - len(self.items))

    def find_item(self, item_id: UUID) -> Optional[InventoryItem]:
        for inv_item in self.items:
            if inv_item.id == item_id:
                return inv_item
        return None

    def get_quantity(self, item_id: UUID) -> int:
        inv_item = self.find_item(item_id)
        return inv_item.quantity if inv_item is not None else 0

    def add_item(self, item: UUID, quantity: int = 1) -> bool:
        """Add an item. If it exists, increase the quantity, if not, add if inventory has space available."""

        # Search if the item is already in the backpack
        if quantity <= 0:
            raise ValueError("Quantity must be equal or greater than 1.")
        
        for inv_item in self.items:
            if inv_item.id == item:
                inv_item.quantity += quantity
                return True

        # If didn't find, looks if there's space available for new slot
        if self.is_full():
            return False

        self.items.append(InventoryItem(id=item, quantity=quantity))
        return True

    def remove_item(self, item: UUID, quantity: int = 1) -> bool:
        """Remove the quantity specified by the item. Returns true if everything was done right, False if there's not the item or the quantity specified."""
        if quantity <= 0:
            raise ValueError("Quantity must be equal or greater than 1.")
    
        for inv_item in self.items:
            if inv_item.id == item:
                if inv_item.quantity < quantity:
                    return False # there's not enough items to remove

                inv_item.quantity -= quantity

                # If the quantity is zero, item disappears from inventory
                if inv_item.quantity == 0:
                    self.items.remove(inv_item)

                return True

        return False # The player doesn't have this item

    # -- equipment slots --

    def get_equipped_item(self, slot: EquipmentSlot) -> Optional[InventoryItem]:
        return self.equipped.get(slot)

    def is_equipped(self, item_id: UUID) -> bool:
        return any(inv_item.id == item_id for inv_item in self.equipped.values())

    def equip_item(
            self,
            item: InventoryItem,
            slot: EquipmentSlot,
    ) -> Optional[InventoryItem]:
        """Equips an item in the slot. Return the previously equipped item, if any."""
        previous = self.equipped.get(slot)
        self.equipped[slot] = item
        return previous

    def unequip_item(self, slot: EquipmentSlot) -> Optional[InventoryItem]:
        """Removes and return the item equipped in the slot, if any."""
        return self.equipped.pop(slot, None)
    