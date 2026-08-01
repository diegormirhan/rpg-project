from enum import StrEnum


class TransactionType(StrEnum):
    TRADE = "trade"
    GIFT = "gift"
    NPC = "npc"