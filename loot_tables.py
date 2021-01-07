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

# print(os.getcwd())

# -- Section 2: Parse Files --

class LootPool:
    def __init__(self, loot_pool)

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

        print(description)




# Extract loot table data from json and reorganize it
def get_loot(filename):
    loot_dict = None
    loot_list = []

    with open(filename) as loot_file:
        loot_dict = json.load(loot_file)
    
    print()
    for pool in loot_dict['pools']:
        for entry in pool['entries']:
            loot_list.append(LootItem(entry))
        
    return loot_list



# -- Section 3: Present Data --

# Testing Code

my_loot = get_loot('MinecraftLootTables/abandoned_mineshaft.json')
for loot in my_loot:
    loot.describe()