from dataclasses import dataclass
from typing import Optional

@dataclass
class ShopItem:
    "An specific item that is been sold in the store"
    id: str
    item_id: str

    # Price in gold to buy
    price_gold: int

    # If the store buys itens from player, then how much it pays?
    sell_back_price: int

    # Stock (if its None, than the item is infinnite, like the life potion)
    stock_quantity: Optional[int] = None

    def can_buy(self, amount: int) -> bool:
        "Checks if the store has enough stock to sell this quantity"
        if self.stock_quantity is None:
            return True

        return self.stock_quantity >= amount

    def process_purchase(self, amount: int) -> None:
        "deducts the stock quantity in the store"
        if self.stock_quantity is not None:
            self.stock_quantity -= amount
            if self.stock_quantity < 0:
                self.stock_quantity = 0

@dataclass
class ShopCatalog:
    "The full catalog from specific store/npc"
    shop_id: str
    name: str

    def calculate_total_cost(self, shop_item: ShopItem, amount: int) -> int:
        "Calculates the total cost from a purchase"
        return shop_item.price_gold * amount