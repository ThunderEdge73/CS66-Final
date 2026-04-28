class SkillNode:
    def __init__(self, name, data):
        self.name = name
        self.cost = data['cost']
        self.parent_name = data['parent'] # String name of the parent
        self.parent_node = None # Actual link to the node object (built later)

class SkillTree:
    def __init__(self, skill_data):
        self.nodes = {}
        # 1. create all nodes
        for name, info in skill_data.items():
            self.nodes[name] = SkillNode(name, info)
        
        # 2. link the nodes (build the tree)
        for node in self.nodes.values():
            if node.parent_name:
                node.parent_node = self.nodes[node.parent_name]


    '''TODO: Implement this function.
    
    You must implement this function RECURSIVELY. 
    It should return true IF AND ONLY IF every ancestor of skill_name is unlocked'''
    def can_unlock(self, skill_name, unlocked_skills):
        current = self.nodes[skill_name]
        if current.name in unlocked_skills or not current.parent_node:
            return True
        if current.parent_name and current.parent_name not in unlocked_skills:
            return False
        return self.can_unlock(current.parent_name, unlocked_skills)