from enum import StrEnum


class ItemType(StrEnum):
    # Main Equipments
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    BOOTS = "boots"
    GLOVES = "gloves"
    SHIELD = "shield"

    # Consumables
    CONSUMABLE = "consumable"

    # Materials
    MATERIAL = "material"
    GEM = "gem"

    # Quest Item
    QUEST_ITEM = "quest_item"