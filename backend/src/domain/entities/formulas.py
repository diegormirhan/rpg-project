from dataclasses import dataclass
    
@dataclass
class CombatFormulas:
    "Centralizes the combat math in the game"
        
    # default critical damage is 150% from normal damage ( 1.5x) 
    base_crit_multiplier: float = 1.5
        
    # min and max chance to land a hit (%)
    min_hit_chance: float = 5.0 
    max_hit_chance: float = 95.0
    
    def calculate_physical_damage(self, attack_power: int, target_defense: int) -> int:
        "Calculates the base damage subtracting the target defense"
        return max(1, attack_power - target_defense)
    
    def is_critical_hit(self, crit_chance_percent: float, rng_roll_function) -> bool:
        "Receives the critical chance from player and rolls the dice"
        roll = rng_roll_function() # Must return from 0 to 100
        return roll <= crit_chance_percent
            
    def calculate_critical_damage(self, base_damage: int) -> int:
        "apply the critical multiplier to the damage you were already going to deal"
        return int(base_damage * self.base_crit_multiplier)
            
    def does_attack_hit(self, accuracy: int, evasion: int, rng_roll_function) -> bool:
        "Calculates if the attack hit or the monster dodged"
        if accuracy + evasion == 0:
            return True
                
        hit_chance = (accuracy / (accuracy + evasion)) * 100.0
            
        hit_chance = max(self.min_hit_chance, min(self.max_hit_chance, hit_chance))
            
        roll = rng_roll_function()
        return roll <= hit_chance