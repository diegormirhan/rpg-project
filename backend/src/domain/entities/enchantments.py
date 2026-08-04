from dataclasses import dataclass, field
from src.domain.enums.enchantment_type import EnchantmentType
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class Enchantment:
    id:  UUID = field(default_factory=uuid4)
    name: str
    description: str
    enchantment_type: EnchantmentType

    # How much power the enchantment gives
    power_value: int

    # The enchantment can have a level. Starts at level 1
    level: int = 1

    # Some enchantments are percentages (True), others have fixed values (False)
    is_percentage: bool = False

    def apply_buff(self, base_value: int) -> int:
        """Receives base value. Returns the new value with enchantment."""
        if self.is_percentage:
            bonus = int(base_value * (self.power_value / 100.0))
            return base_value + bonus
        else:
            return base_value + self.power_value
        