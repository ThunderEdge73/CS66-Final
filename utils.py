import json
import requests
import random 

def load_game_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_safe_input(raw_input):
    cleaned = raw_input.strip().lower()
    return "BLANK_COMMAND" if not cleaned else cleaned


def generate_character_name(name_parts):
    name = random.choice(name_parts["Names"])
    
    prefix = ""
    if random.random() < 0.75: 
        prefix = random.choice(name_parts["Prefixes"]) + " "
        
    suffix = ""
    if random.random() < 0.75:
        suffix = " " + random.choice(name_parts["Suffixes"])
        
    return prefix + name + suffix


def get_weather_modifier(zipcode, api_key):
    # Put the relevant part(s) of your homework 3 solution here, if you want to incorporate that - but that's not part of the assignment.
    pass

"""TODO: Implement this function
        Sorts the enemies by the specified key and returns a sorted list.
        By the way, almost identical to the mergeSort function we saw in class, with very small modifications that greatly generalize it.
        Remember, enemies are dictionaries with keys like "Name", "hp", etc.
"""
def mergeSort(all_enemies, key):
    if len(all_enemies) <= 1:
        return all_enemies
    start, mid, end = 0, len(all_enemies) // 2, len(all_enemies)
    l1 = mergeSort(all_enemies[start:mid], key)
    l2 = mergeSort(all_enemies[mid:end], key)
    return merge_lists(l1, l2, key)

def merge_lists(list1, list2, key):
    final_list = []
    i1 = 0
    i2 = 0
    while len(list1) != i1 or len(list2) != i2:
        if len(list1) == i1:
            final_list.append(list2[i2])
            i2 += 1
        elif len(list2) == i2:
            final_list.append(list1[i1])
            i1 += 1
        else:
            item1 = list1[0]
            item2 = list2[0]
            if item1[key] < item2[key]:
                final_list.append(list1[i1])
                i1 += 1
            else:
                final_list.append(list2[i2])
                i2 += 1
    return final_list

"""TODO: Implement this function
        Generates a nice-looking string of enemies sorted by the provided key (hp, attack, etc.).
        If you wanted to later generalize this - to sort and summarize other kinds of data (reachable locations, for example, you could).
"""
def get_tactical_report(all_enemies, key):
    sorted_enemies = mergeSort(all_enemies, key)
    final_string = ""
    for enemy in sorted_enemies:
        name = enemy["name"]
        data = enemy[key]
        final_string += f"{name}: {data} {key}\n"
    return final_string[:-1]
