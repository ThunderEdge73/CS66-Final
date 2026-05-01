import time

def run_battle(hero, enemy, party):
    print(f"\n--- BATTLE STARTED: {hero.name} vs {enemy.name} ---")
    
    party_members = party.get_allies()
    if len(party_members) == 0:
        combatants = [hero, enemy]
        ally_one = None
        ally_two = None
    elif len(party_members) == 1:
        ally_one = party_members[0]
        ally_two = None
        combatants = [hero, enemy, ally_one]
    elif len(party_members) == 2:
        ally_one = party_members[0]
        ally_two = party_members[1]
        combatants = [hero, enemy, ally_one, ally_two]
    
     # If you wanted more combatants per fight, you could think about various ways to do that.
    
    # SORTING: Order by speed descending. And no, you may not .sort() your way out of the main sorting problem in this assignment.
    combatants.sort(key=lambda x: x.speed, reverse=True)
    
    print(f"Initiative Order: {[c.name for c in combatants]}")
    
    while hero.hp > 0 and enemy.hp > 0:
        for entity in combatants:
            if entity.hp <= 0: continue 
            
            if ally_one == None and ally_two == None:
                #battle with no allies
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
            if ally_one != None and ally_two == None:
                #battle with one ally
                if entity == hero:
                    print(f"\nYour turn! (HP: {hero.hp})")
                    input("Press Enter to Attack...") 
                    dmg = hero.attack
                    enemy.take_damage(dmg)
                    print(f"You hit {enemy.name} for {dmg} damage!")
                elif entity == ally_one:
                    dmg = ally_one.attack
                    enemy.take_damage(dmg)
                    print(f"\n{ally_one.name} attacks for {dmg} damage!")
                else:
                    print(f"\n{enemy.name} attacks!")
                    dmg = enemy.attack
                    hero.hp -= dmg
                    print(f"You took {dmg} damage!")
            if ally_two != None and ally_one != None:
                #battle with two allies
                if entity == hero:
                    print(f"\nYour turn! (HP: {hero.hp})")
                    input("Press Enter to Attack...") 
                    dmg = hero.attack
                    enemy.take_damage(dmg)
                    print(f"You hit {enemy.name} for {dmg} damage!")
                elif entity == ally_one:
                    dmg = ally_one.attack
                    enemy.take_damage(dmg)
                    print(f"\n{ally_one.name} attacks for {dmg} damage!")
                elif entity == ally_two:
                    dmg = ally_two.attack
                    enemy.take_damage(dmg)
                    print(f"\n{ally_two.name} attacks for {dmg} damage!")
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