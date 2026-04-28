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