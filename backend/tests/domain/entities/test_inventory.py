import pytest
from uuid import uuid4

from src.domain.entities.inventory import Inventory, InventoryItem
from src.domain.entities.items import Item
from src.domain.entities.player import Player
from src.domain.enums.character_class import CharacterClass
from src.domain.enums.equipment_slot import EquipmentSlot
from src.domain.enums.item_rarity import ItemRarity
from src.domain.enums.item_type import ItemType
from src.domain.exceptions import (
    ClassRestrictionError,
    InventoryFullError,
    ItemAlreadyEquippedError,
    ItemNotEquippableError,
    ItemNotEquippedError,
    ItemNotFoundError,
    LevelRequirementError,
)
from src.domain.services.inventory_service import InventoryService

@pytest.fixture
def player() -> Player:
    return Player(
        user_id="user-1",
        name="Hero",
        character_class=CharacterClass.KNIGHT,
        level=5
    )

@pytest.fixture
def inventory() -> Inventory:
    return Inventory(player_id="user-1", max_slots=3)

@pytest.fixture
def service() -> InventoryService:
    return InventoryService()

def make_item(item_type: ItemType, **kwargs) -> Item:
    return Item(
        id=kwargs.pop("id", uuid4()),
        name=kwargs.pop("name", "Item"),
        description="Test item",
        item_type=item_type,
        rarity=kwargs.pop("rarity", ItemRarity.COMMON),
        **kwargs,
    )

def make_sword(**kwargs) -> Item:
    kwargs.setdefault("name", "sword")
    kwargs.setdefault("attack_bonus", 10)
    return make_item(ItemType.WEAPON, **kwargs)


# ------ Inventory Entity -------

def test_add_new_item_creates_entry(inventory: Inventory) -> None:
    item_id = uuid4()
    assert inventory.add_item(item_id, 2) is True
    entry = inventory.find_item(item_id)
    assert entry is not None
    assert entry.quantity == 2


def test_add_existing_item_increments_quantity(inventory: Inventory) -> None:
    item_id = uuid4()
    inventory.add_item(item_id, 2)
    assert inventory.add_item(item_id, 3) is True
    assert inventory.get_quantity(item_id) == 5
    assert len(inventory.items) == 1


def test_add_when_full_returns_false(inventory: Inventory) -> None:
    inventory.add_item(uuid4())
    inventory.add_item(uuid4())
    inventory.add_item(uuid4())
    assert inventory.is_full()
    assert inventory.add_item(uuid4()) is False


def test_add_rejects_quantity_zero(inventory: Inventory) -> None:
    with pytest.raises(ValueError):
        inventory.add_item(uuid4(), 0)


def test_remove_item_decrements_quantity(inventory: Inventory) -> None:
    item_id = uuid4()
    inventory.add_item(item_id, 5)
    assert inventory.remove_item(item_id, 2) is True
    assert inventory.get_quantity(item_id) == 3


def test_remove_item_removes_entry_when_zero(inventory: Inventory) -> None:
    item_id = uuid4()
    inventory.add_item(item_id, 1)
    assert inventory.remove_item(item_id, 1) is True
    assert inventory.find_item(item_id) is None


def test_remove_item_insufficient_returns_false(inventory: Inventory) -> None:
    item_id = uuid4()
    inventory.add_item(item_id, 1)
    assert inventory.remove_item(item_id, 2) is False


def test_remove_missing_item_returns_false(inventory: Inventory) -> None:
    assert inventory.remove_item(uuid4(), 1) is False


def test_available_slots(inventory: Inventory) -> None:
    assert inventory.available_slots() == 3
    inventory.add_item(uuid4())
    assert inventory.available_slots() == 2


def test_equip_item_returns_displaced(inventory: Inventory) -> None:
    old = InventoryItem(id=uuid4(), quantity=1)
    new = InventoryItem(id=uuid4(), quantity=1)
    assert inventory.equip_item(old, EquipmentSlot.WEAPON) is None
    assert inventory.equip_item(new, EquipmentSlot.WEAPON) is old
    assert inventory.get_equipped_item(EquipmentSlot.WEAPON) is new


def test_unequip_item_returns_and_clears(inventory: Inventory) -> None:
    entry = InventoryItem(id=uuid4(), quantity=1)
    inventory.equip_item(entry, EquipmentSlot.HEAD)
    assert inventory.unequip_item(EquipmentSlot.HEAD) is entry
    assert inventory.get_equipped_item(EquipmentSlot.HEAD) is None


def test_is_equipped(inventory: Inventory) -> None:
    item_id = uuid4()
    inventory.equip_item(InventoryItem(id=item_id, quantity=1), EquipmentSlot.BODY)
    assert inventory.is_equipped(item_id) is True
    assert inventory.is_equipped(uuid4()) is False

# ---------- item Entity -----------------

@pytest.mark.parametrize(
    "item_type, expected_slot",
    [
        (ItemType.WEAPON, EquipmentSlot.WEAPON),
        (ItemType.ARMOR, EquipmentSlot.BODY),
        (ItemType.HELMET, EquipmentSlot.HEAD),
        (ItemType.BOOTS, EquipmentSlot.BOOTS),
        (ItemType.GLOVES, EquipmentSlot.GLOVES),
        (ItemType.SHIELD, EquipmentSlot.SHIELD),
    ],
)
def test_resolve_equipment_slot_from_type(
    item_type: ItemType, expected_slot: EquipmentSlot
) -> None:
    item = make_item(item_type)
    assert item.is_equippable() is True
    assert item.resolve_equipment_slot() == expected_slot

def test_resolve_explicit_equipment_slot_takes_priority() -> None:
    item = make_item(ItemType.WEAPON, equipment_slot=EquipmentSlot.SHIELD)
    assert item.resolve_equipment_slot() == EquipmentSlot.SHIELD

def test_consumable_is_not_equippable() -> None:
    item = make_item(ItemType.CONSUMABLE)
    assert item.is_equippable() is False
    assert item.is_consumable() is True


# ---------- InventoryService: equip ---------

def test_equip_success(inventory, player, service) -> None:
    sword = make_sword()
    inventory.add_item(sword.id)

    equipped = service.equip(player, inventory, sword)

    assert equipped is inventory.get_equipped_item(EquipmentSlot.WEAPON)
    assert inventory.find_item(sword.id) is None
    assert inventory.is_equipped(sword.id) is True


def test_equip_swap_returns_old_item_to_backpack(inventory, player, service) -> None:
    old_sword = make_sword(name="Old Sword", attack_bonus=5)
    new_sword = make_sword(name="New Sword", attack_bonus=15)
    inventory.add_item(old_sword.id)
    service.equip(player, inventory, old_sword)
    inventory.add_item(new_sword.id)

    service.equip(player, inventory, new_sword)

    equipped = inventory.get_equipped_item(EquipmentSlot.WEAPON)
    assert equipped is not None
    assert equipped.id == new_sword.id
    assert inventory.get_quantity(old_sword.id) == 1
    assert inventory.find_item(new_sword.id) is None


def test_equip_swap_with_full_backpack_succeeds(inventory, player, service) -> None:
    old_sword = make_sword(name="Old Sword")
    new_sword = make_sword(name="New Sword")
    potion = make_item(ItemType.CONSUMABLE)
    extra = make_item(ItemType.CONSUMABLE)
    inventory.add_item(old_sword.id)
    service.equip(player, inventory, old_sword)
    inventory.add_item(new_sword.id)
    inventory.add_item(potion.id)
    inventory.add_item(extra.id)

    assert inventory.is_full()

    service.equip(player, inventory, new_sword)

    equipped = inventory.get_equipped_item(EquipmentSlot.WEAPON)
    assert equipped is not None
    assert equipped.id == new_sword.id
    assert len(inventory.items) == 3
    assert inventory.get_quantity(old_sword.id) == 1
    assert inventory.get_quantity(potion.id) == 1


def test_equip_non_equippable_item_raises(inventory, player, service) -> None:
    potion = make_item(ItemType.CONSUMABLE)
    inventory.add_item(potion.id)
    with pytest.raises(ItemNotEquippableError):
        service.equip(player, inventory, potion)


def test_equip_item_not_in_inventory_raises(inventory, player, service) -> None:
    sword = make_sword()
    with pytest.raises(ItemNotFoundError):
        service.equip(player, inventory, sword)


def test_equip_already_equipped_raises(inventory, player, service) -> None:
    sword = make_sword()
    inventory.add_item(sword.id)
    service.equip(player, inventory, sword)
    with pytest.raises(ItemAlreadyEquippedError):
        service.equip(player, inventory, sword)


def test_equip_level_too_low_raises(inventory, player, service) -> None:
    sword = make_sword(level_requirement=10)
    inventory.add_item(sword.id)
    with pytest.raises(LevelRequirementError):
        service.equip(player, inventory, sword)


def test_equip_class_restriction_raises(inventory, player, service) -> None:
    sword = make_sword(class_restriction=CharacterClass.NECROMANCER)
    inventory.add_item(sword.id)
    with pytest.raises(ClassRestrictionError):
        service.equip(player, inventory, sword)


def test_equip_allows_same_class(inventory, player, service) -> None:
    sword = make_sword(class_restriction=CharacterClass.KNIGHT)
    inventory.add_item(sword.id)
    assert service.equip(player, inventory, sword).id == sword.id


# ---------- InventoryService: unequip ----------

def test_unequip_success(inventory, player, service) -> None:
    sword = make_sword()
    inventory.add_item(sword.id)
    service.equip(player, inventory, sword)

    returned = service.unequip(inventory, EquipmentSlot.WEAPON)

    assert returned.id == sword.id
    assert inventory.get_equipped_item(EquipmentSlot.WEAPON) is None
    assert inventory.get_quantity(sword.id) == 1


def test_unequip_empty_slot_raises(inventory, service) -> None:
    with pytest.raises(ItemNotEquippedError):
        service.unequip(inventory, EquipmentSlot.WEAPON)


def test_unequip_when_backpack_full_raises(inventory, player, service) -> None:
    sword = make_sword()
    inventory.add_item(sword.id)
    service.equip(player, inventory, sword)
    inventory.add_item(uuid4())
    inventory.add_item(uuid4())
    inventory.add_item(uuid4())
    assert inventory.is_full()

    with pytest.raises(InventoryFullError):
        service.unequip(inventory, EquipmentSlot.WEAPON)