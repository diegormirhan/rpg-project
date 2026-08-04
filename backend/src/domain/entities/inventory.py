from dataclasses import dataclass, field
from typing import List, Dict
from uuid import UUID, uuid4

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

    def is_full(self) -> bool:
        # Checks if inventory is full
        return len(self.items) >= self.max_slots

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

