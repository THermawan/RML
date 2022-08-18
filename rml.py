from RMLGen import RMLGen as RMLGen

# Error message.
def rand_err():
    print('\nHey pal, you gotta tell me what to randomize, yeah?\n')

    print('Try RAND ALL to get a completely random spec,')
    print('or RAND <LEVEL> if yer wantin\' a specific loot level.')

# Specify paths here!
rar_src = 'rarities.txt'
man_src = 'manufacturers.txt'
loot_src = 'loot.txt'
lweight_src = 'loot_weights.txt'
level_map = 'levels_to_rarity.txt'

# Build generator here.
gen = RMLGen(rar_src, man_src, loot_src, lweight_src, level_map)

# ================================================
# WELCOME TO YOUR FOUNDRY TERMINAL.
# ================================================
comm = input('> ').upper().strip()

while comm != 'QUIT':
    comm = comm.split() if len(comm.split()) else ['']

    # Option 1: Generate something!
    if comm[0] == 'RAND':

        # Failsafe in case you accidentally entered just 'RAND' for some reason.
        # Technically in OO you'd build a class to handle this but why bother lol.
        if len(comm) < 2:
            rand_err()

        # Randomize everything. Don't care about levels!
        elif comm[1] == 'ALL':
            print(gen.rand_all())

        # Set a level to randomize the item at. If it's not a valid integer, I will cry.
        else:
            try:
                level = int(comm[1])
                print(gen.rand_level(level))

            except ValueError:
                rand_err()


    # Option 2: List everything you've just generated.
    elif comm[0] == 'HIST' and len(comm) == 1:
        gen.print_repo()

    # Option 3: Reset history.
    elif comm[0] == 'RESET' and len(comm) == 1:
        print(gen.reset_repo())

    # Invalid comm message.
    else:
        print('SURE THING, BUDDY.')

    print()
    comm = input('> ').upper().strip()

print('\nEND PROGRAM.')
