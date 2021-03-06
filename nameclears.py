# Modify parameters here #

INIT_COUNT = 2254
DEPTH = 30
OUTPUTFILE = "nameclears_output.txt"

#All names must be spelled correctly and the first letter must be uppercase
REQUIRED_DJINN = {}    # Syntax : {"Dew", "Flash", "Granite"}
DISPLAYED_DJINN = {}   # Syntax : {"Dew", "Flash", "Granite"}
MIN_ELEM_COUNTS = {}   # Syntax : {"Mercury": 5, "Jupiter": 5}
PASSWORD = False       # Set to True to for bronze password runs

# Syntax : "Name": [HP, PP, ATK, DEF, AGI, LCK],
REQUIRED_STATS = {
    "Isaac": [0, 0, 122, 0, 0, 0],
    "Felix": [0, 0, 32, 0, 27, 0],
    "Jenna": [0, 0, 0, 0, 28, 0],
    "Sheba": [0, 42, 0, 0, 30, 0],
}

# Syntax : "Name": [HP, PP, ATK, DEF, AGI, LCK],
# Use 1 for true and 0 for false
DISPLAYED_STATS = {
    "Isaac": [0, 0, 1, 0, 0, 0],
    "Felix": [0, 0, 1, 0, 1, 0],
    "Jenna": [0, 0, 0, 0, 1, 0],
    "Sheba": [0, 1, 0, 0, 1, 0],
}

# end of modifiable region #


# RNG solving functions #

def construct_RN_list(multiplier, increment):
    multList = [multiplier]
    incList = [increment]
    for i in range(31):
        multList.append((multList[i]**2) & 0xFFFFFFFF)
        incList.append((multList[i]*incList[i]+incList[i]) & 0xFFFFFFFF)
    return multList,incList

def find_value(count, initValue=0):
    for i in range(32):
        if (count >> i) & 1:
            initValue = (initValue*multipliers[i] + increments[i]) & 0xFFFFFFFF
    return initValue

def find_count(value):
    advances = 0
    for i in range(32):
        if value & 2**i:
            value = (value*multipliers[i] + increments[i]) & 0xFFFFFFFF
            advances += 2**i
    return -advances & 0xFFFFFFFF

multipliers,increments = construct_RN_list(0x41c64e6d, 0x3039)


# Stat Calculation #

Party1 = {"Isaac", "Garet", "Ivan", "Mia"}
Party2 = {"Felix", "Jenna", "Sheba", "Piers"}

Goal_Values = {
    "Isaac": [
        [30, 182, 334, 486, 638, 790],
        [20, 80, 130, 170, 210, 250],
        [13, 86, 162, 237, 313, 388],
        [6, 38, 69, 102, 134, 166],
        [8, 86, 163, 241, 318, 396],
        [3, 3, 3, 3, 3, 3],
        ],
    "Garet": [
        [33, 191, 351, 510, 670, 830],
        [18, 76, 124, 162, 200, 238],
        [11, 83, 156, 228, 301, 373],
        [8, 41, 75, 110, 144, 179],
        [6, 76, 144, 212, 281, 349],
        [2, 2, 2, 2, 2, 2],
        ],
    "Ivan": [
        [28, 166, 304, 442, 581, 719],
        [24, 92, 150, 196, 242, 288],
        [8, 76, 144, 211, 277, 344],
        [4, 35, 65, 95, 124, 155],
        [11, 91, 173, 255, 337, 419],
        [4, 4, 4, 4, 4, 4],
        ],
    "Mia": [
        [29, 173, 317, 462, 606, 751],
        [23, 90, 146, 190, 235, 280],
        [9, 79, 150, 220, 289, 359],
        [5, 37, 68, 100, 131, 163],
        [7, 80, 152, 224, 296, 369],
        [5, 5, 5, 5, 5, 5],
        ],
    "Felix": [
        [32, 187, 342, 498, 654, 810],
        [19, 78, 127, 166, 205, 244],
        [13, 87, 164, 240, 316, 392],
        [6, 38, 70, 103, 135, 168],
        [7, 83, 158, 232, 307, 382],
        [2, 2, 2, 2, 2, 2],
        ],
    "Jenna": [
        [29, 177, 326, 474, 622, 770],
        [21, 85, 138, 180, 223, 265],
        [10, 81, 153, 224, 295, 366],
        [5, 37, 69, 101, 132, 165],
        [8, 85, 162, 238, 315, 392],
        [4, 4, 4, 4, 4, 4],
        ],
    "Sheba": [
        [28, 169, 311, 452, 593, 735],
        [24, 91, 148, 193, 238, 284],
        [8, 78, 147, 215, 283, 351],
        [4, 36, 66, 98, 128, 159],
        [10, 88, 168, 248, 328, 407],
        [5, 5, 5, 5, 5, 5],
        ],
    "Piers": [
        [30, 184, 337, 491, 644, 798],
        [19, 79, 129, 168, 208, 248],
        [11, 82, 155, 226, 298, 370],
        [7, 39, 72, 106, 139, 173],
        [6, 78, 148, 218, 289, 359],
        [3, 3, 3, 3, 3, 3],
        ],
}

LevelUps = {
    "Isaac": 28,
    "Garet": 28,
    "Ivan" : 28,
    "Mia"  : 28,
    "Felix": 5,
    "Jenna": 5,
    "Sheba": 5,
    "Piers": 18,
}


def get_stats(g_count):

    g_value = find_value(g_count)
    PartyStats = {}

    def grn():
        nonlocal g_value, g_count
        g_count += 1
        g_value = (g_value * 0xc64e6d + 0x3039) & 0xFFFFFF
        return (g_value >> 8) & 0xFFFF

    for name, statlist in Goal_Values.items():
        PartyStats[name] = [statlist[i][0] for i in range(6)]
        for level in range(LevelUps[name]):
            level_index = (level+1) // 20
            for stat in range(6):
                goals = statlist[stat]
                difference = goals[level_index + 1] - goals[level_index]
                PartyStats[name][stat] += (difference + (grn()*20 >> 16)) // 20
    
    return PartyStats


# Djinn Calculation #

Djinn = [
    ["Flint","Granite","Quartz","Vine","Sap","Ground","Bane","Echo","Iron","Steel","Mud","Flower","Meld","Petra","Salt","Geode","Mold","Crystal",],
    ["Fizz","Sleet","Mist","Spritz","Hail","Tonic","Dew","Fog","Sour","Spring","Shade","Chill","Steam","Rime","Gel","Eddy","Balm","Serac",],
    ["Forge","Fever","Corona","Scorch","Ember","Flash","Torch","Cannon","Spark","Kindle","Char","Coal","Reflux","Core","Tinder","Shine","Fury","Fugue",],
    ["Gust","Breeze","Zephyr","Smog","Kite","Squall","Luff","Breath","Blitz","Ether","Waft","Haze","Wheeze","Aroma","Whorl","Gasp","Lull","Gale",],
]

Elements = {"Venus":0, "Mercury":1, "Mars":2, "Jupiter":3}


# $080B1290: +14 per element, +2 per Djinn index
DjinnPercents = [
    [100, 70, 70, 30, 40, 50, 20],
    [100, 50, 70, 70, 30, 30, 70],
    [70, 50, 30, 60, 70, 40, 70],
    [50, 50, 70, 50, 20, 70, 70],
]


def get_djinn(g_count):
    global Djinn, DjinnPercents

    g_value = find_value(g_count) & 0xFFFFFF
    current_djinn = {"Flint", "Fizz"}
    elem_counts = [1,1,0,0]
    djinn_to_add = 16

    def grn():
        nonlocal g_value, g_count
        g_count += 1
        g_value = (g_value * 0xc64e6d + 0x3039) & 0xFFFFFF
        return (g_value >> 8) & 0xFFFF

    while djinn_to_add:
        element = grn()*4 >> 16
        index = grn()*7 >> 16
        name = Djinn[element][index]
        if elem_counts[element] == min(elem_counts) and name not in current_djinn:
            if grn()*100 >> 16 < DjinnPercents[element][index]:
                current_djinn.add(name)
                elem_counts[element] += 1
                djinn_to_add -= 1

    return current_djinn, elem_counts, g_count


# Recursive pathfinding function
def get_successes(g_count, depth, path=""):
    global Successes, Checked, Elements, REQUIRED_DJINN, DISPLAYED_DJINN, Party1, Party2
    if g_count in Checked: 
        return
    else: 
        Checked.add(g_count)
    djinn, elem_counts, new_count = get_djinn(g_count)
    if REQUIRED_DJINN.issubset(djinn) and all(elem_counts[Elements[k]] >= v for k, v in MIN_ELEM_COUNTS.items()):
        stats = get_stats(g_count - 1126)
        # Account for asynchronous stat calculation for bronze password runs
        if PASSWORD:
            if all(stats[name][i] >= REQUIRED_STATS[name][i] for name in REQUIRED_STATS.keys() & Party2 for i in range(6)):
                init_stats = stats.copy()
                p_clears = 0
                while p_clears < depth:
                    stats = get_stats(g_count + (p_clears+1)*1126)
                    if all(stats[name][i] >= REQUIRED_STATS[name][i] for name in REQUIRED_STATS.keys() & Party1 for i in range(6)):
                        for name in Party2: stats[name] = init_stats[name]
                        Successes.append([f"{path} + P*{p_clears}", stats, g_count + (p_clears+1)*1126, djinn])
                    p_clears += 1
        elif all(stats[name][i] >= REQUIRED_STATS[name][i] for name in REQUIRED_STATS for i in range(6)):
            Successes.append([path, stats, g_count, djinn])
    if depth > 0: 
        get_successes(g_count + 1126, depth-1, path + "F")
        get_successes(new_count + 1126, depth-1, path + "I")



import sys, time, traceback
sys.setrecursionlimit(1100)

# Typecast to sets in case the user tries '{}' to make an empty set
REQUIRED_DJINN, DISPLAYED_DJINN = set(REQUIRED_DJINN), set(DISPLAYED_DJINN)

try:
    print("Calculating...")
    init_time = time.time()
    Successes = []
    Checked = set()
    get_successes(INIT_COUNT, DEPTH)  # This does all the searching; updates Successes and Checked lists
    Successes = sorted(Successes, key=lambda x: x[2])  # Sorts the entries by g_count

    with open(OUTPUTFILE, "w") as f:  # Writes and formats data
        for path, stats, g_count, djinn in Successes:
            f.write(path + ":\n")
            for name, flag_list in DISPLAYED_STATS.items():
                for flag, stat_type, stat in zip(flag_list, ["HP", "PP", "ATK", "DEF", "AGI", "LCK"], stats[name]):
                    if flag: f.write(f"  {name[:2]} {stat_type}: {stat},")
            f.write(f"\n  GRN: 0x{find_value(g_count):0>8X}  Gcount: {g_count}\n  Other: {djinn & DISPLAYED_DJINN or ''}\n\n")

except Exception as e:
    print(traceback.format_exc())
else:
    print(f"""\
    Completed search at depth {DEPTH}
    Elapsed time: {time.time() - init_time}
    Outputted successfully to {OUTPUTFILE}""")
