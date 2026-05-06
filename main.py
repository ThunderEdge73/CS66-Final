from utils import load_game_data, get_safe_input, generate_character_name, get_tactical_report
from entities import Hero, Enemy, Ally
from world_graph import build_world
from skill_tree import SkillTree
from combat import run_battle
from storage import save_game, load_game
import random
# yo
#yoyo
# yo yo yo
def main():
    print(".::..::. A Perilous Journey .::..::.")
    data = load_game_data("game_data.json")
    
    # Initialize the skill tree (You have some stuff TODO in the skill_tree class)
    skill_tree = SkillTree(data['assets']['skills'])
    
    # and build the environment (TODO) (which is a graph, containing locations and connections between locations)
    game_world = build_world() 
    
    # Show the map at startup (optional but helpful - do you know what function needs to be defined for this to work?)
    print(game_world) 

    # Character creation or loading
    hero = None
    cmd = input("Type 'load' to resume or 'new' to start: ").strip().lower()
    
    if cmd == 'load':
        hero = load_game()
        
    if not hero:
        # 1. Ask for a name
        print("\n--- CHARACTER CREATION ---")
        raw_name = input("Enter your hero's name (or press Enter for a random name): ")
        clean_name = get_safe_input(raw_name)
        
        final_name = ""
        
        if clean_name == "BLANK_COMMAND": # Generate a random name
            name_parts = data['assets']['names']
            final_name = generate_character_name(name_parts)
            print(f" The Fates have chosen. You are {final_name}.")
        else: # Clean up the provided name a little
            final_name = raw_name.strip().title() # Here's a nifty function you might not have seen yet.
            print(f"Welcome, {final_name}!")

        # 3. Instantiate Hero
        hero = Hero(final_name, data['assets']['base_stats']) # this is a little different previous assignments: we are passing a dict of base stats now, rather than the entire data object. 
        
        # 4. Set Starting Location (using the game_world object)
        if "Town" in game_world.locations:
            hero.location = game_world.locations["Town"]
        else:
            first_key = list(game_world.locations.keys())[0]
            hero.location = game_world.locations[first_key]
            
        print("New game started.")
    # MAIN LOOP: This is where the game processes users' inputs one at a time.
    while True:
        # Show Context (Graph Node info)
        print(f"---------------------------\nLOCATION: {hero.location}")
        
        raw = input("\nCommand (Type help for a list of all commands): ")
        command = get_safe_input(raw)
        
        parts = command.split() # For example, the command might be "move north" - then parts = ["move", "north"]
        action = parts[0]
        
        # Movement (where you can move depends on the topology of the game, i.e. the World graph)
        if action == "move":
            if len(parts) < 2:
                print("Move where?")
                continue
            direction = str.capitalize(parts[1])
            # Check Graph Adjacency
            if direction in hero.location.connections:
                hero.location = hero.location.connections[direction]["target"]
                print(f"You moved {direction}...")
            else:
                print("You cannot go that way.")

        # Combat
        elif action == "fight":
            # Spawn a random enemy for demo purposes - there are a lot of ways to make this smarter and more specific to location!
            
            e_data = random.choice(data['assets']['enemies'])
            enemy = Enemy(e_data['name'], e_data)
            
            victory = run_battle(hero, enemy, hero.party)
            if not victory:
                break # Game Over

        # Skills
        elif action == "skill":
            if len(parts) < 2:
                skills_list = ""
                for skill in hero.skills_unlocked.keys():
                    skills_list += f"{skill} | "
                print("Known skills: " + skills_list)
                print(f"Current mana: {hero.mana}")
                print(f"Available skills: {skill_tree.available_skills(hero)}")
                continue
            skill_name = parts[1].capitalize()

            if skill_name in hero.skills_unlocked:
                print("You already know that.")
            
            # This is something you must TODO before it works - implement can_unlock, recursively.
            else:
                can_unlock_skill = skill_tree.can_unlock(skill_name, hero)
                if can_unlock_skill == True:
                    hero.learn_skill(skill_tree.nodes[skill_name])
                elif can_unlock_skill == "pre-req":
                    print("You cannot learn that yet. (Prerequisites missing!)")
                elif can_unlock_skill == "level":
                    print("You cannot learn that yet. (Level is too low!)")
                elif can_unlock_skill == "mana":
                    print("You cannot learn that yet. (Insufficient mana!)")

        elif action == "heal":
            if len(parts) < 2:
                heal_skills = "Healing skills available: "
                for i in hero.skills_unlocked:
                    if i == "Dia":
                        heal_skills += "Dia: +30 HP, 3 Mana "
                    elif i == "Diarama":
                        heal_skills += "| Diarama: +60 HP, 6 Mana "
                    elif i == "Diarahan":
                        heal_skills += "| Diarahan: FULL HP, 12 Mana"
                if heal_skills == "Healing skills available: ":
                    heal_skills += "None"
                print(heal_skills)
                continue
            heal = parts[1].capitalize()
            if heal not in ["Dia", "Diarama", "Diarahan"]:
                print("Invalid skill")
            else:
                if hero.hp == hero.max_hp:
                    print("You are already fully healed.")
                elif heal in hero.skills_unlocked:
                    if hero.mana < skill_tree.nodes[heal].use_cost:
                        print("Insufficient mana")
                    else:
                        hero.hp += int(skill_tree.nodes[heal].effect[0])
                        hero.mana -= skill_tree.nodes[heal].use_cost
                        if hero.hp > hero.max_hp:
                            hero.hp = hero.max_hp
                        print(f"You healed! HP: {hero.hp} / {hero.max_hp}")
                else:
                    print("You do not have that skill unlocked.")

        elif action == "scan":
            #TODO: Implement the scan command to show a tactical report of the current location using the get_tactical_report function from utils.py
            # You need to identify the right set of enemies (the ones at the location the hero is currently in)
            # You need to correctly get the second argument from the user input, which is something like "scan hp" or "scan attack". (Hint: look at how the variable action is obtained, above.). Once you have it, this is the key according to which you should sort.
            # Then all you really need to do is make sure your sorting method is correctly implemented, in utils.py
            if len(parts) < 2:
                print(f"What stat to scan for?")
                continue
            checked_stat = parts[1].lower()
            if checked_stat not in ["hp", "attack", "speed"]:
                print(f"Invalid stat to scan")
                continue
            print(get_tactical_report(hero.location.enemies, checked_stat))
        elif action == "path":
            if len(parts) != 3:
                continue
            start = game_world.locations[parts[1].title()]
            end = game_world.locations[parts[2].title()]
            print(game_world.get_path(start, end)[1])
        elif action == "talk":
            creature = hero.location.allies
            ally_data = data["assets"]["allies"]
            for i in range(len(ally_data)):
                ally_creature = [ally_data[i]["name"]]
                if ally_creature == creature:
                    ally = Ally(ally_data[i]["name"], ally_data[i]["hp"], ally_data[i]["attack"], ally_data[i]["speed"])
            ally_raw = input(f"\nWould you like to add {ally.name} to your party? [yes, no]: ")
            ally_command = get_safe_input(ally_raw)
            if ally_command == "no":
                print(f"You did not add {ally.name} to your party.")
            else: 
                x = hero.party.add_member(ally)
                print(x)
                if x == "Party limit reached.":
                    print(hero.party)
                    party_raw = input(f"\nWould you like to replace a party member? [yes, no]: ")
                    party_command = get_safe_input(party_raw)
                    if party_command == "yes":
                        replace_command = int(input(f"\nWhich member would you like to replace? [1, 2]: "))
                        if replace_command == 1:
                            y = hero.party.replace_member(hero.party.members[0], ally)
                            print(y)
                        else: 
                            hero.party.remove_member(hero.party.members[1])
                            y = hero.party.add_member(ally)
                            print(y)
        #  Saving and loading the game is done through serialization, a technique we have not learned. You can see more
        # of this technique in CS 67! For now, you can just use the functions I've provided in storage.py.
        # A cool way to improve this would be to also save other parts of the game state - the world, etc.
        # You could try your hand at this without really understanding the details involved, if you wanted.
        # But do that separately from this assignment.
        elif action == "save":
            save_game(hero)
        elif action == "exit":
            print("Goodbye.")
            break
        elif action == "world":
            print("")
            print(game_world)
        elif action == "help":
            print("""
move [direction] -> Move in the specified direction.
skill [name?] -> If name is specified, tries to unlock the skill with the provided name.
    Otherwise, will display all learned/available skills.
fight -> Initiates a fight in the current area against an enemy.
scan [stat] -> Scan the current area
talk -> Talk to a potential ally
world -> Display the current world.
save -> Save the game.
exit -> Exit the game.\n""")
            print(hero)

        elif action == "xp":
            hero.xp.gain_xp(95, hero)

        elif action == "mana":
            hero.mana += 50

        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()