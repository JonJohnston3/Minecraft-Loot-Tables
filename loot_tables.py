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

class LootItem:
    def __init__(self, loot_entry):
        self.type = loot_entry.get('type').replace('minecraft:', '')
        self.weight = loot_entry.get('weight', 1)
        self.functions = loot_entry.get('functions', None)
        self.name = loot_entry.get('name','empty_slot').replace('minecraft:', '')

        if self.functions is not None:
            self.parse_functions(self.functions)
    
    def __repr__(self):
        return self.name + " loot object"

    def parse_functions(self):
        



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
        
    for loot in loot_list:
        print(loot)
    return loot_list

get_loot('MinecraftLootTables/abandoned_mineshaft.json')

# -- Section 3: Present Data --