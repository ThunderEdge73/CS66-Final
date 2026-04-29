from utils import load_game_data, get_safe_input, generate_character_name, get_tactical_report
from entities import Hero, Enemy
from world_graph import build_world
from skill_tree import SkillTree
from combat import run_battle
from storage import save_game, load_game
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
        print(f"\nLOCATION: {hero.location}")
        
        raw = input("\nCommand (move [dir], scan [stat], fight, skill [name], save, exit): ")
        command = get_safe_input(raw)
        
        parts = command.split() # For example, the command might be "move north" - then parts = ["move", "north"]
        action = parts[0]
        
        # Movement (where you can move depends on the topology of the game, i.e. the World graph)
        if action == "move":
            if len(parts) < 2:
                print("Move where?")
                continue
            direction = parts[1]
            # Check Graph Adjacency
            if direction in hero.location.connections:
                hero.location = hero.location.connections[direction]["target"]
                print(f"You moved {direction}...")
            else:
                print("You cannot go that way.")

        # Combat
        elif action == "fight":
            # Spawn a random enemy for demo purposes - there are a lot of ways to make this smarter and more specific to location!
            import random
            e_data = random.choice(data['assets']['enemies'])
            enemy = Enemy(e_data['name'], e_data['hp'], e_data['attack'], e_data['speed'])
            
            victory = run_battle(hero, enemy)
            if not victory:
                break # Game Over

        # Skills
        elif action == "skill":
            if len(parts) < 2:
                print(f"Known skills: {hero.skills_unlocked}")
                continue
            skill_name = parts[1].capitalize()

            if skill_name in hero.skills_unlocked:
                print("You already know that.")
            
            # This is something you must TODO before it works - implement can_unlock, recursively.
            elif skill_tree.can_unlock(skill_name, hero.skills_unlocked):
                # (We skip XP cost checks for this demo to focus on game logic)
                # But it'd be cool to have that. Otherwise it's kind of trivial to have skill unlocks at all.
                # You could implement this if you wanted.
                hero.learn_skill(skill_name)
                print(f"You learned {skill_name}!")
            else:
                print("You cannot learn that yet (Prerequisites missing!).")
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
        
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()