from containers import *

class Enemy:
    def __init__(self, name, enemy_stats):
        self.name = name
        self.hp = enemy_stats['hp']
        self.attack = enemy_stats['attack']
        self.speed = enemy_stats['speed']
        self.xp = enemy_stats['hp']
        self.mana = enemy_stats['attack']
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0: self.hp = 0

    def __str__(self):
        return f"[ENEMY] {self.name} (HP: {self.hp})"
    
class Ally:
    def __init__(self, name, hp, attack, speed):
        '''
        Creates the ally
        Parameters: ally name, hp, attack and speed. From game_data.json
        Returns: nothing
        O(1) all cases
        '''
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.max_hp = hp

    def take_damage(self, amount):
        '''
        Assigns damage to the ally
        Parameters: the amount the ally is taking
        O(1) all cases
        '''
        self.hp -= amount
        if self.hp < 0: self.hp = 0
    
    def __str__(self):
        '''
        prints the ally and their stats
        Returns: string to be printed
        O(1)
        '''
        return f"[ALLY] {self.name} | HP: {self.hp} | ATK: {self.attack} | SPD: {self.speed}"

class Hero:
    def __init__(self, name, base_stats):
        self.name = name
        self.hp = base_stats['hp']
        self.max_hp = base_stats['max_hp']
        self.defense = base_stats['defense']
        self.attack = base_stats['attack']
        self.strength = base_stats['strength']
        self.mana = base_stats['mana']
        self.luck = base_stats['luck']
        self.xp = XPBar()
        self.level = 1
        self.speed = base_stats['speed'] # This decides whether you or your enemy strikes first
        self.party = Party()
        
        # (Assignment 4 stuff)
        self.inventory = []       
        self.quest_log = QuestLog() 
  
        # (New stuff)
        self.skills_unlocked = {} 
        self.location = None 

    def learn_skill(self, skill):
        self.skills_unlocked[skill.name] = skill
        self.mana -= skill.cost
        if skill.type == "passive":
            self.process_skill(skill)
        else:
            print(f"You learned {skill.name}!")

    def process_skill(self, skill):
        effect = skill.effect
        modifier = float(effect[1])
        stat = effect[2]
        return_string = f"You learned {skill.name}! "
        if stat == "max_hp":
            self.max_hp += int(modifier)
            return_string += f"MAX HP increased by {int(modifier)}"
        elif stat == "speed":
            self.speed += int(modifier)
            return_string += f"SPD increased by {int(modifier)}"
        elif stat == "luck":
            self.luck += modifier
            return_string += f"LUCK increased by {modifier}"
        print(return_string)
    
    def log_event(self, description):
        self.quest_log.add_entry(description)
    
    def level_up_message(self, message):
        return_string = f"You leveled up! LVL: {self.level} | Stat Growth:"
        for stat in message:
            if stat == "max_hp":
                return_string += "\nMAX HP increased by 10"
            elif stat == "attack":
                return_string += "\nATK increased by 1"
            elif stat == "speed":
                return_string += "\nSPD increased by 2"
            else:
                return_string += "\nLUCK increased by 0.2"
        print(return_string)

    def __str__(self):
        return f"[HERO] {self.name} \nHP: {self.hp} / {self.max_hp} \nMANA: {self.mana} | ATK: {self.attack} \nSPD: {self.speed} | LUCK: {self.luck} \n{self.xp} \n\nParty: \n{self.party}"

    def __add__(self, item):
        self.inventory.append(item)
        return self
    
class Party:
    #Creates a party for the hero which is limited to two members
    def __init__(self):
        '''
        Creates an empty party
        No parameters needed
        Returns nothing
        O(1) all cases
        '''
        self.limit = 2
        self.members = []

    def add_member(self, ally):
        '''
        adds a new ally to the party
        Paramters: ally being added to the party
        Returns: results of operation
        O(1) all cases
        '''
        party_limit = self.check_limit()#checks if the maximum allowed members of the party has been reached
        if party_limit == True: 
            return "Party limit reached." #does not allow if limit reached
        else:
            self.members.append(ally) #if space available ally is added to party
            self.length += 1
            return f"{ally.name} has been added to the party."

    def remove_member(self, ally):
        '''
        removes an ally from the party
        Parameters: ally being removed from the party
        Returns: nothing
        #O(1) best case
        #O(n) worst case: technically limited to O(1) in the implementation but will increase as such if party limit increases
        '''
        self.members.remove(ally)
        self.length -= 1

    def replace_member(self, ally_replace, ally_insert):
        '''
        replaces a member of the party with a new member
        Parameters: ally being replaced and ally being inserted
        Returns: the results of adding the new member (should always return a string saying the ally was added to the party)
        O(1) best case
        O(n) worst case (same scenario as remove_member)
        '''
        self.remove_member(ally_replace)
        return self.add_member(ally_insert)
    
    def get_allies(self):
        '''
        used to create a list of combatants for combat
        Returns: list of party members
        O(1) all cases
        '''
        return self.members

    def check_limit(self):
        '''
        checks if the party limit has been reached
        Parameters: none
        Returns: True if limit has been reached, False if limit has not been reached
        O(1) all cases
        '''
        if self.limit == self.length:
            return True
        else:
            return False
        
    def __str__(self):
        '''
        Prints the members of the of the party and their stats
        Returns: a string of what is being printed
        O(n) all cases
        '''
        party_print = ""
        if self.members == []:
            party_print = "You have no party members"
        else:
            for i in range(self.members):
                x = str(print(self.members[i]))
                party_print += f"{x} \n"
        return party_print