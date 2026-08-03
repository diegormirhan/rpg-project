from dataclasses import dataclass, field
from typing import List

@dataclass
class Zone:
    id: str
    name: str
    description: str

    # Acess control
    min_level_required: int = 1

    # If false, players can attack eachother here
    is_safe_zone: bool = True

    # Which monsters exists in this part of map (Keep their ID's)
    spawnable_monster_ids: List[str] = field(default_factory=list)

    # How much monsters can be alive at the same time here
    max_monsters_alive: int = 10

    def can_player_enter(self, player_level: int) -> bool:
        "Verify if player can survive and enter in the zone"
        return player_level >= self.min_level_required

    def is_pvp_allowed(self) -> bool:
        "reverse the safe zone logic to becode easier to read in combat. If its NOT safe zone, the PVP is open"
        return not self.is_safe_zone