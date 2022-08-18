from random import randint as randint

class RMLGen:
    # Constructor. Reads from all those config files we have.
    def __init__(self, rar_src, man_src, loot_src, lweight_src, level_map):
        # Pull config files here. Assumption all paths correct.
        self.rarities = [rarity.rstrip() for rarity in open(rar_src, 'r')]
        self.manufacturers = [man.rstrip() for man in open(man_src, 'r')]

        self.rar_weights = {}    # Store level to rarity weighting.
        self.loot_weights = {}   # Store level to loot weighting.
        self.loot = {}           # Store loot to manufacturer mapping.
        self.repo = []           # Store everything produced so far.

        # Process rarity weights per level.
        level = 0
        for line in open(level_map, 'r'):
            # Each line reps a loot level.
            # Each value on each line (separated by commas) reps a rarity weighting.
            self.rar_weights[level] = [int(weight.strip()) for weight in line.split(',')]
            level += 1

        # Process loot weights per level.
        level = 0
        for line in open(lweight_src, 'r'):
            self.loot_weights[level] = [int(weight.strip()) for weight in line.split(',')]
            level += 1

        # Process eligible manufacturers per loot type.
        for line in open(loot_src, 'r'):
            line = line.split('|')
            key = line[0].rstrip()

            # I'll do this in two steps for readability.
            # Step 1: Interpret each set of indices after 'loot.txt' as integers so Python won't yell at me.
            legit = [int(idx.strip())-1 for idx in line[1].split(',')]

            # Step 2: Turn those indices to manufacturers.
            legit = [self.manufacturers[idx] for idx in legit]

            self.loot[key] = legit

        self.max_lvl = len(self.rar_weights)-1

    # Ticks down along a seed value until it hits 0. Selects a value corresponding to the index it stops on.
    def countdown(self, seed, range, values):
        i = 0
        while seed > 0:
            if seed <= range[i]:
                return values[i]

            seed -= range[i]
            i = (i + 1) % len(range)

    # Randomizes a level, then generates a weapon.
    def rand_all(self):
        level = randint(0, self.max_lvl)
        return self.rand_level(level)

    # Generates a weapon based on a given level.
    def rand_level(self, level):
        if level > self.max_lvl or level < 0:
            return '\nYOU ARE NOT AUTHORISED TO USE THAT LEVEL.'

        num = len(self.repo) + 1
        r_range = self.rar_weights[level]
        l_range = self.loot_weights[level]

        rar = self.countdown(randint(1, 20), r_range, self.rarities)
        ltype = self.countdown(randint(1, 100), l_range, list(self.loot.keys()))

        model = self.loot[ltype][randint(0, len(self.loot[ltype])-1)]

        ret = f'{num}. L{level}: {rar} {model} {ltype}'
        self.repo.append(ret)
        return ret

    # Print repo.
    def print_repo(self):
        if not self.repo:
            print('\nYOU DO NOT HAVE ANY WEAPONS IN YOUR INVENTORY.')

        for weapon in self.repo:
            print(weapon)
