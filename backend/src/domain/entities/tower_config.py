from dataclasses import dataclass
from typing import List

@dataclass
class TowerFloor:
    "Represents a unique floor from the challenge tower"
    floor_number: int

    # Which monster shows in this floor (can be a boss)
    monster_id: str

    # Bonus reward for clearing the floor for the first time
    first_clear_gold: int
    first_clear_item_id: str


@dataclass
class TowerConfig:
    "Manages the rules of how all the tower works"
    id: str
    name: str
    description: str

    # Min level to be able to enter first floor
    min_level_entry: int

    # List of all configured towers in the game
    floors: List[TowerFloor]

    def can_player_enter(self, player_level: int) -> bool:
        "The player is strong enough to enter the floor?"
        return player_level >= self.min_level_entry

    def get_floor_details(self, floor_number: int) -> TowerFloor | None:
        "Search for the specific floor config details"
        for floor in self.floors:
            if floor.floor_number == floor_number:
                return floor

        return None # Player reached max floor