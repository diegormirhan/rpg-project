from dataclasses import dataclass

@dataclass
class XPCalculator:
    """Class responsible for all math involved on XP and Levels"""

    # How much base xp needs to reach level 2
    base_xp_requirement: int = 100

    # Multiplier
    # 1.5 means that every level needs at least 50% more XP than the previous level
    difficulty_multiplier: float = 1.5

    # Max level in the game
    max_level: int = 200

    def get_xp_needed_for_level(self, level: int) -> int:
        """Returns how much total XP is necessary to achieve the given level."""
        if level == 1:
            return 0
        if level > self.max_level:
            level = self.max_level

        # exponencial formula: Base XP * (Multiplier ^ (Level - 2))
        return int(self.base_xp_requirement * (self.difficulty_multiplier ** (level - 2)))

    def check_level_up(self, current_level: int, current_xp: int) -> bool:
        """Checks if the XP quantity that player has is enough to get him to the next level"""
        if current_xp <= 0:
            raise ValueError("XP must be greater than 0.")
    
        if current_level >= self.max_level:
            return False

        xp_needed = self.get_xp_needed_for_level(current_level + 1)
        return current_xp >= xp_needed