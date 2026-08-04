from dataclasses import dataclass, field
from src.domain.enums.character_class import CharacterClass
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class ClassDefinition:
    """Define the rules and base attributes from a class in the game."""
    id: UUID = field(default_factory=uuid4)
    class_type: CharacterClass
    name: str
    description: str

    # Initial attributes Level 1
    base_hp: int
    base_mana: int

    # Growth by level
    hp_per_level: int
    mana_per_level: int

    starting_weapon_id: str
    starting_armos_id: str

    def calculate_max_hp(self, level: int) -> int:
        """Calculate the max hp from a class on specified level."""
        # on level 1, player has base_hp. Starting at level 2, player has hp_per_level
        return self.base_hp + (self.hp_per_level * (level - 1))

    def calculate_max_mana(self, level: int) -> int:
        """calculate the max mana from a class on specified level."""
        # on level 1, player has base_mana. Starting at level 2, player has mana_per_level
        return self.base_mana + (self.mana_per_level * (level - 1))