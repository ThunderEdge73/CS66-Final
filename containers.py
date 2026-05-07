import random
class Quest:
    """A basic unit of a QuestLog - it's basically a node."""
    def __init__(self, data):
        self.data = data
        self.next = None

class QuestLog:
    """A custom linked list container to store the hero's Quests."""
    def __init__(self):
        self.head = None
        self._size = 0

    """Adds a new Quest entry to the front of the log."""
    def add_entry(self, text):
        new_quest = Quest(text)
        new_quest.next = self.head
        self.head = new_quest
        self._size += 1

    def __len__(self):
        return self._size

    def __str__(self):
        quest_strings = []
        current = self.head
        while current is not None:
            quest_strings.append(str(current.data))
            current = current.next
            
        if not quest_strings:
            return "No quests recorded."
        return " -> ".join(quest_strings)

class XPBar:
    def __init__(self):
        '''
        Creates the XP Bar
        No parameters or return values
        O(1)
        '''
        self.progress = 0
        self.cap = 100
        self.level = 1
        self.level_cap = False

    def gain_xp(self, amount, hero):
        '''
        Adds xp to the bar
        Parameters: amount of xp being added, hero the xp bar belongs to
        Returns: nothing
        All cases: O(1)
        '''
        if self.level_cap == False:
            self.progress += amount
            if self.progress >= self.cap:#initiates level up if required xp has been reached
                self.level_up(hero)
    
    def level_up(self, hero):
        '''
        Executes the level up for the hero and xp_bar
        Parameters: Hero xp is being added to
        Returns: nothing
        All cases: O(1)
        '''
        self.level += 1
        hero.level += 1
        if hero.level == 6: #hero level limit is 6
            self.level_cap = True
            self.progress = 0
        else:
            self.progress -= self.cap #resets level progress plus the extra xp before level up
            self.cap *= 1.5 #increase required xp
            level_up_message = []
            for i in range(3): #adds heros stat buffs
                stat = random.choice(["max_hp", "attack", "speed", "luck"])
                if stat == "max_hp":
                    hero.max_hp += 10
                    level_up_message.append("max_hp")
                elif stat == "attack":
                    hero.attack += 1
                    level_up_message.append("attack")
                elif stat == "speed":
                    hero.speed += 2
                    level_up_message.append("speed")
                elif stat == "luck":
                    hero.luck += 0.2
                    level_up_message.append("luck")
            hero.level_up_message(level_up_message)#creates level up message
    
    def __repr__(self): 
        '''
        Prints the users level and how much until their next level
        Parameters and Returns: none
        All cases: O(1)
        '''
        if self.level_cap == True:
            return f"LVL: {self.level} | AT LEVEL CAP"
        else:
            return f"LVL: {self.level} | XP: {self.cap - self.progress} Until next level"