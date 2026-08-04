from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class ShopItem:
    """An specific item that is been sold in the store."""
    id: UUID = field(default_factory=uuid4)
    item_id: UUID

    # Price in gold to buy
    price_gold: int

    # If the store buys itens from player, then how much it pays?
    sell_back_price: int

    # Stock (if its None, than the item is infinnite, like the life potion)
    stock_quantity: Optional[int] = None

    def can_buy(self, amount: int) -> bool:
        """Checks if the store has enough stock to sell this quantity"""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        
        if self.stock_quantity is None:
            return True

        return self.stock_quantity >= amount

    def process_purchase(self, amount: int) -> None:
        """Deducts the stock quantity in the store."""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        
        if self.stock_quantity is not None:
            self.stock_quantity -= amount
            if self.stock_quantity < 0:
                self.stock_quantity = 0

@dataclass(kw_only=True)
class ShopCatalog:
    """The full catalog from specific store/npc."""
    id: UUID = field(default_factory=uuid4)
    name: str
    items_for_sale: List[ShopItem] = field(default_factory=list)

    def calculate_total_cost(self, shop_item: ShopItem, amount: int) -> int:
        """Calculates the total cost from a purchase."""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        
        return shop_item.price_gold * amount