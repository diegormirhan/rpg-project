from src.domain.entities.inventory import Inventory, InventoryItem
from src.domain.entities.items import Item
from src.domain.entities.player import Player
from src.domain.enums.equipment_slot import EquipmentSlot
from src.domain.exceptions import (
    ClassRestrictionError,
    InventoryFullError,
    ItemAlreadyEquippedError,
    ItemNotEquippableError,
    ItemNotEquippedError,
    ItemNotFoundError,
    LevelRequirementError
)


class InventoryService:
    """Bsuniss rules for equipping and unequipping items."""

    def equip(
            self,
            player: Player,
            inventory: Inventory,
            item: Item
    ) -> InventoryItem:
        """Equips an item. If the target slot is occupied, the old item returns to the backpack."""
        item_id = item.id

        if not item.is_equippable():
            raise ItemNotEquippableError(item_id)

        slot = item.resolve_equipment_slot()
        if slot is None:
            raise ItemNotEquippableError(item_id)

        if player.level < item.level_requirement:
            raise LevelRequirementError(item.level_requirement, player.level)

        if item.class_restriction is not None and item.class_restriction != player.character_class:
            raise ClassRestrictionError(item.class_restriction, player.character_class)

        if inventory.is_equipped(item_id):
            raise ItemAlreadyEquippedError(item_id)

        entry = inventory.find_item(item_id)
        if entry is None:
            raise ItemNotFoundError(item_id)

        previous = inventory.get_equipped_item(slot)

        # removing a sing unit only frees a slot when the entry has quantity 1
        freed_slots = 1 if entry.quantity == 1 else 0
        if previous is not None and inventory.available_slots() + freed_slots < 1:
            raise InventoryFullError()

        fresh = InventoryItem(id=item_id, quantity=1)
        inventory.remove_item(item_id, 1)
        inventory.equip_item(fresh, slot)

        if previous is not None:
            inventory.add_item(previous.id, previous.quantity)

        return fresh

    def unequip(
            self,
            inventory: Inventory,
            slot: EquipmentSlot,
    ) -> InventoryItem:
        """Removes the item from the slot and puts it back in the backpack."""
        entry = inventory.get_equipped_item(slot)
        if entry is None:
            raise ItemNotEquippedError(slot)

        if inventory.available_slots() < 1:
            raise InventoryFullError()

        inventory.unequip_item(slot)
        inventory.add_item(entry.id, entry.quantity)

        return entry