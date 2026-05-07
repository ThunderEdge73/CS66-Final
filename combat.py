import time
from utils import get_safe_input

def run_battle(hero, enemy, party):
    "Modified the battle loop to include party members and extra hero actions for battle"
    "O(nlogn) because of the sort statement and number of combatants"
    print(f"\n--- BATTLE STARTED: {hero.name} vs {enemy.name} ---")
    party_members = party.get_allies()
    #sets a list of combatants based on the length of the party coordinating to each ally
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
    combatState = {
        "hero": hero,
        "allies": party_members,
        "enemy": enemy
    }

    hero.strength = 1
    hero.defense = 1
    guard = False

    print(f"Initiative Order: {[c.name for c in combatants]}")
    
    while hero.hp > 0 and enemy.hp > 0:
        for entity in combatants:
            if entity.hp <= 0: continue 
            
            if ally_one == None and ally_two == None:
                #battle with no allies
                if entity == hero:
                    if guard == True: #turns off the heros guard (activated via action command)
                        guard = False
                        hero.defense -= 1
                    print(f"\nYour turn! (HP: {hero.hp} / {hero.max_hp}, MANA: {hero.mana})")
                    action = get_action(hero) #instead of attacking allows players to utilize new commands
                    if action[0] == "attack":
                        dmg = round(hero.attack * hero.strength) #attack is now combined with hero strength
                        enemy.take_damage(dmg)
                        print(f"You hit {enemy.name} for {dmg} damage!")
                    elif action[0] == "skill":
                        skill = hero.skills_unlocked[action[1].capitalize()] #use skills in skill tree
                        if skill.type == 'attack':
                            dmg = round(int(skill.effect[0]) * hero.strength)
                            hero.mana -= skill.use_cost #each skill has a manna cost associated with it
                            enemy.take_damage(dmg)
                            print(f"You hit {enemy.name} for {dmg} damage!")
                        elif skill.type == 'heal': #allows hero to heal mid battle
                            hero.hp += int(skill.effect[0])
                            hero.mana -= skill.use_cost
                            if hero.hp > hero.max_hp:
                                hero.hp = hero.max_hp
                            print(f"You healed! HP: {hero.hp} / {hero.max_hp}")
                        elif skill.type == 'buff': #allows you to increase hero stats using skills
                            if len(skill.effect) == 3:
                                hero.strength += 0.75
                                hero.defense += 0.75
                                hero.mana -= 20
                            elif skill.effect[1] == 'strength':
                                hero.strength += float(skill.effect[0])
                                hero.mana -= skill.use_cost
                            elif skill.effect[1] == 'defense':
                                hero.defense += float(skill.effect[0])
                                hero.mana -= skill.use_cost
                    elif action[0] == "defend": #sets heros guard to on
                        guard = True
                        hero.defense += 1
                else:
                    print(f"\n{enemy.name} attacks!")
                    dmg = round(enemy.attack / hero.defense)
                    hero.hp -= dmg
                    print(f"You took {dmg} damage!")
            if ally_one != None and ally_two == None:
                #battle with one ally
                if entity == hero: #hero and enemy actions function the same as in a 1v1 battle
                    if guard == True:
                        guard = False
                        hero.defense -= 1
                    print(f"\nYour turn! (HP: {hero.hp} / {hero.max_hp}, MANA: {hero.mana})")
                    action = get_action(hero)
                    if action[0] == "attack":
                        dmg = round(hero.attack * hero.strength)
                        enemy.take_damage(dmg)
                        print(f"You hit {enemy.name} for {dmg} damage!")
                    elif action[0] == "skill":
                        skill = hero.skills_unlocked[action[1].capitalize()]
                        if skill.type == 'attack':
                            dmg = round(int(skill.effect[0]) * hero.strength)
                            hero.mana -= skill.use_cost
                            enemy.take_damage(dmg)
                            print(f"You hit {enemy.name} for {dmg} damage!")
                        elif skill.type == 'heal':
                            hero.hp += int(skill.effect[0])
                            hero.mana -= skill.use_cost
                            if hero.hp > hero.max_hp:
                                hero.hp = hero.max_hp
                            print(f"You healed! HP: {hero.hp} / {hero.max_hp}")
                        elif skill.type == 'buff':
                            if len(skill.effect) == 3:
                                hero.strength += 0.75
                                hero.defense += 0.75
                                hero.mana -= 20
                            elif skill.effect[1] == 'strength':
                                hero.strength += float(skill.effect[0])
                                hero.mana -= skill.use_cost
                            elif skill.effect[1] == 'defense':
                                hero.defense += float(skill.effect[0])
                                hero.mana -= skill.use_cost
                    elif action[0] == "defend":
                        guard = True
                        hero.defense += 1
                elif entity == ally_one:
                    #ally acts in the same manner as the enemy but attacking the enemy rather than the hero
                    dmg = ally_one.attack
                    enemy.take_damage(dmg)
                    print(f"\n{ally_one.name} attacks for {dmg} damage!")
                else:
                    print(f"\n{enemy.name} attacks!")
                    dmg = round(enemy.attack / hero.defense)
                    hero.hp -= dmg
                    print(f"You took {dmg} damage!")
            if ally_two != None and ally_one != None:
                #battle with two allies
                if entity == hero:
                    if guard == True:
                        guard = False
                        hero.defense -= 1
                    print(f"\nYour turn! (HP: {hero.hp} / {hero.max_hp}, MANA: {hero.mana})")
                    action = get_action(hero)
                    if action[0] == "attack":
                        dmg = round(hero.attack * hero.strength)
                        enemy.take_damage(dmg)
                        print(f"You hit {enemy.name} for {dmg} damage!")
                    elif action[0] == "skill":
                        skill = hero.skills_unlocked[action[1].capitalize()]
                        if skill.type == 'attack':
                            dmg = round(int(skill.effect[0]) * hero.strength)
                            hero.mana -= skill.use_cost
                            enemy.take_damage(dmg)
                            print(f"You hit {enemy.name} for {dmg} damage!")
                        elif skill.type == 'heal':
                            hero.hp += int(skill.effect[0])
                            hero.mana -= skill.use_cost
                            if hero.hp > hero.max_hp:
                                hero.hp = hero.max_hp
                            print(f"You healed! HP: {hero.hp} / {hero.max_hp}")
                        elif skill.type == 'buff':
                            if len(skill.effect) == 3:
                                hero.strength += 0.75
                                hero.defense += 0.75
                                hero.mana -= 20
                            elif skill.effect[1] == 'strength':
                                hero.strength += float(skill.effect[0])
                                hero.mana -= skill.use_cost
                            elif skill.effect[1] == 'defense':
                                hero.defense += float(skill.effect[0])
                                hero.mana -= skill.use_cost
                    elif action[0] == "defend":
                        guard = True
                        hero.defense += 1
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
                    dmg = round(enemy.attack / hero.defense)
                    hero.hp -= dmg
                    print(f"You took {dmg} damage!")
                
            time.sleep(0.5) 

    if hero.hp > 0:
        print(f"VICTORY! You defeated {enemy.name}. Gained {round(enemy.xp * hero.luck)} XP and {round(enemy.mana * hero.luck)} MANA") # If you wanted to implement a looting system, you could do so here.
        hero.log_event(f"Defeated {enemy.name}") # Add it to the hero's QuestLog
        hero.xp.gain_xp(enemy.xp * hero.luck, hero)
        hero.mana += enemy.mana * hero.luck
        return True
    else:
        print("DEFEAT... Game Over.")
        return False

def get_action(hero):
    '''
    Allows users to access extra commands in the battle sequence
    Parameters: none
    Returns: the action the user wants to use
    Best Case: O(1)
    Worst Case: O(n)
    '''
    valid_action = False
    while not valid_action: #while loop until the user enters a valid command
        action = get_safe_input(input("\nWhat will you do? [attack, skill (name), defend]... ")).split()
        if action[0] in ["attack", "defend"]:
            valid_action = True
            continue
        elif action[0] == "skill":
            if len(action) == 1: #scenario in which user enters "skill" 
                skills_list = "Avilable skills: "
                for skill in hero.skills_unlocked.values():
                    if skill == "Luster Candy":
                        skills_list += "Luster_candy: 0.75 Strength/Defense, 20 Mana | "
                    elif skill.type != "passive":
                        skills_list += f"{skill.name}: {skill.effect[0]} {skill.effect[1]}, {skill.use_cost} Mana | "
                print(f"{skills_list} \n") #gives the user a list of available skills that are not passive
                continue
            elif len(action) == 2:# when user enters "skill name"
                if action[1].capitalize() in hero.skills_unlocked:
                    current_skill = hero.skills_unlocked[action[1].capitalize()]
                    #various situations in which the user's choice of action is redundant
                    if current_skill.use_cost > hero.mana:
                        print("Insufficient mana!\n")
                        continue
                    if current_skill.type == "heal" and hero.hp == hero.max_hp:
                        print("You are already fully healed.\n")
                        continue
                    if current_skill.effect[1] == "strength" and hero.strength >= 1.75:
                        print("You are at the strength limit.\n")
                        continue
                    if current_skill.effect[1] == "defense" and hero.defense >= 1.75:
                        print("You are at the defense limit.\n")
                        continue
                    if len(current_skill.effect) == 3 and hero.defense >= 1.75:
                        print("You are at the defense limit.\n")
                    valid_action = True
                    continue
                else: #These commands prevent the user from entering an invalid command in various situations
                    print("You do not know that skill.")
                    continue
            else:
                print("Invalid skill name. (Try using underscores instead of a space!)")
        else:
            print("Invalid command.\n")
            continue
    return action