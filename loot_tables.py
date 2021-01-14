from contextlib import contextmanager
import os
import json

# -- Section 1: Find Files --

# Establish change directory function cd() to allow through the with context manager
# Takes string input as windows formatted path
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)



# -- Section 2: Parse Files --

# Class for entire loot table
class LootTable:
    def __init__(self, filename):
        self.name = filename.replace('.json','').replace('_', ' ')
        with open(filename) as loot_file:
            self.parse_dict(json.load(loot_file))        

    def __repr__(self):
        return self.name + ' loot table'
    
    def parse_dict(self, loot_dict):
        self.loot_pools = []
        self.type = loot_dict.get('type').replace('minecraft:','')
        for pool in loot_dict.get('pools'):
            self.loot_pools.append(LootPool(pool))
    
    def describe(self):
        description = "{name} loot table containing {count} loot pool(s)\n".format(name = self.name.title(), count = len(self.loot_pools))
        for i in range(len(self.loot_pools)):
            description += str(i + 1) + '. ' + self.loot_pools[i].describe()
        return description

# Class for loot pool in loot table
class LootPool:
    def __init__(self, loot_pool):
        self.parse_rolls(loot_pool.get('rolls'))
        self.parse_entries(loot_pool.get('entries'))

    def parse_rolls(self, rolls):
        if type(rolls) is dict:
            self.min_rolls = rolls.get('min')
            self.max_rolls = rolls.get('max')
        else:
            self.min_rolls = rolls
            self.max_rolls = rolls

    def parse_entries(self, entries):
        self.entries = []
        for entry in entries:
            self.entries.append(LootItem(entry))

    def describe(self):
        description = "Pool using "
        if self.min_rolls == self.max_rolls:
            description += str(self.min_rolls) + ' roll(s) '
        else:
            description += str(self.min_rolls) + ' to ' + str(self.max_rolls) + ' rolls '
        description += 'with the loot set:\n'
        for entry in self.entries:
            description += '\t' + entry.describe() + '\n'
        return description


# Class for individual item in loot pool
class LootItem:
    min = None
    max = None

    def __init__(self, loot_entry):
        self.type = loot_entry.get('type').replace('minecraft:', '')
        self.weight = loot_entry.get('weight', 1)
        self.functions = loot_entry.get('functions', None)
        self.name = loot_entry.get('name','empty_slot').replace('minecraft:', '')

        if self.functions is not None:
            self.parse_functions()
    
    def __repr__(self):
        return self.name + " loot object"

    # Converts item functions into object attributes
    def parse_functions(self):
        function_list = []

        for function in self.functions:
            if function['function'] == 'minecraft:enchant_randomly':
                function_list.append('enchant_randomly')
            elif function['function'] == 'minecraft:set_count':
                function_list.append('set_count')
                self.min = function['count']['min']
                self.max = function['count']['max']

        self.functions = function_list

    # Prints loosely formatted string describing the loot object
    # !!Rewrite to use .format() for legibility!!
    def describe(self):
        description = ""
        if self.functions:
            for function in self.functions:
                if function == 'set_count':
                    description += (str(self.min) + ' to ' + str(self.max) + ' ')
                elif function == 'enchant_randomly':
                    description += 'randomly enchanted '
        
        description += self.name.replace('_', ' ')
        description += ' with weight ' + str(self.weight)

        return description




# Extract loot table data from json and reorganize it
def get_loot(filename):
    loot_dict = None
    loot_pools = []

    with open(filename) as loot_file:
        loot_dict = json.load(loot_file)
    
    for pool in loot_dict['pools']:
        loot_pools.append(LootPool(pool))
        
    return loot_pools



# -- Section 3: Present Data --

# Testing Code

print(os.getcwd())
with cd('C:/Users/Jon/Documents/Loot Tables/chests'):
    for file in os.listdir(os.getcwd()):
        filename = os.fsdecode(file)
        print(filename)
    #print(os.getcwd())

# my_loot = LootTable('MinecraftLootTables/abandoned_mineshaft.json')
# print(my_loot.describe())