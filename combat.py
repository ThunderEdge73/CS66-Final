import time

def run_battle(hero, enemy):
    print(f"\n--- BATTLE STARTED: {hero.name} vs {enemy.name} ---")
    
    combatants = [hero, enemy] # If you wanted more combatants per fight, you could think about various ways to do that.
    
    # SORTING: Order by speed descending. And no, you may not .sort() your way out of the main sorting problem in this assignment.
    combatants.sort(key=lambda x: x.speed, reverse=True)
    
    print(f"Initiative Order: {[c.name for c in combatants]}")
    
    while hero.hp > 0 and enemy.hp > 0:
        for entity in combatants:
            if entity.hp <= 0: continue 
            
            if entity == hero:
                print(f"\nYour turn! (HP: {hero.hp})")
                input("Press Enter to Attack...") 
                dmg = hero.attack
                enemy.take_damage(dmg)
                print(f"You hit {enemy.name} for {dmg} damage!")
            else:
                print(f"\n{enemy.name} attacks!")
                dmg = enemy.attack
                hero.hp -= dmg
                print(f"You took {dmg} damage!")
                
            time.sleep(0.5) 

    if hero.hp > 0:
        print(f"VICTORY! You defeated {enemy.name}.") # If you wanted to implement a looting system, you could do so here.
        hero.log_event(f"Defeated {enemy.name}") # Add it to the hero's QuestLog
        return True
    else:
        print("DEFEAT... Game Over.")
        return False