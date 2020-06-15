# Modify parameters here #

INIT_COUNT = 2254
DEPTH = 30
OUTPUTFILE = "NameClears_Output.txt"
required_djinn = {}    #Syntax : {"Dew", "Flash", "Granite"}
displayed_djinn = {}   #Syntax : {"Dew", "Flash", "Granite"}
min_elem_counts = {}   #Syntax : {"Mercury": 5, "Jupiter": 5}

#Syntax : "Name": [HP, PP, ATK, DEF, AGI, LCK],
required_stats = {
    "Isaac": [0, 0, 122, 0, 0, 0],
    "Felix": [0, 0, 32, 0, 27, 0],
    "Jenna": [0, 0, 0, 0, 28, 0],
    "Sheba": [0, 42, 0, 0, 30, 0],
}
#Syntax : "Name": [positionlist],
displayed_stats = {
    "Isaac": [2],
    "Felix": [2, 4],
    "Jenna": [4],
    "Sheba": [1, 4],
}

# end #


def constructRNlist(multiplier, increment):
    multList = [multiplier]
    incList = [increment]
    for i in range(31):
        multList.append((multList[i]**2) & 0xFFFFFFFF)
        incList.append((multList[i]*incList[i]+incList[i]) & 0xFFFFFFFF)
    return multList,incList

def findValue(count, initValue=0):
    for i in range(32):
        if (count >> i) & 1:
            initValue = (initValue*multipliers[i] + increments[i]) & 0xFFFFFFFF
    return initValue

def findCount(value):
    advances = 0
    for i in range(32):
        if value & 2**i:
            value = (value*multipliers[i] + increments[i]) & 0xFFFFFFFF
            advances += 2**i
    return -advances & 0xFFFFFFFF

multipliers,increments = constructRNlist(0x41c64e6d, 0x3039)


# This section is for calculating stats #

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
    "Ivan": 28,
    "Mia": 28,
    "Felix": 5,
    "Jenna": 5,
    "Sheba": 5,
    "Piers": 18,
}


def Get_Stats(g_count):

    g_value = findValue(g_count)
    PartyStats = {
        "Isaac": [],
        "Garet": [],
        "Ivan": [],
        "Mia": [],
        "Felix": [],
        "Jenna": [],
        "Sheba": [],
        "Piers": [],
    }

    def grn():
        nonlocal g_value, g_count
        g_count += 1
        g_value = (g_value * 0xc64e6d + 0x3039) & 0xFFFFFF
        return (g_value >> 8) & 0xFFFF

    for name in PartyStats.keys():
        PartyStats[name] = list(next(zip(*Goal_Values[name])))
        for level in range(LevelUps[name]):
            level_index = (level+1) // 20
            for stat in range(6):
                goals = Goal_Values[name][stat]
                difference = goals[level_index + 1] - goals[level_index]
                PartyStats[name][stat] += (difference + (grn()*20 >> 16)) // 20
    
    return PartyStats

# end #


# This section is for calculating Djinn #

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


def Get_Djinn(g_count):
    global Djinn, DjinnPercents

    g_value = findValue(g_count) & 0xFFFFFF
    CurrentDjinn = {"Flint", "Fizz"}
    ElemCounts = [1,1,0,0]
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
        if ElemCounts[element] == min(ElemCounts) and name not in CurrentDjinn:
            if grn()*100 >> 16 < DjinnPercents[element][index]:
                CurrentDjinn.add(name)
                ElemCounts[element] += 1
                djinn_to_add -= 1

    return CurrentDjinn, ElemCounts, g_count


def getSuccesses(g_count, depth, path=""):
    global Successes, Checked, Elements, required_djinn, displayed_djinn
    if g_count in Checked: return
    else: Checked.add(g_count)
    djinn, elem_counts, new_count = Get_Djinn(g_count)
    if required_djinn.issubset(djinn) and all(elem_counts[Elements[k]] >= v for k, v in min_elem_counts.items()):
        stats = Get_Stats(g_count - 1126)
        if all(stats[name][i] >= required_stats[name][i] for name in required_stats for i in range(6)):
            Successes.append([path, stats, g_count, djinn])
    if depth > 0: 
        getSuccesses(g_count + 1126, depth-1, path + "F")
        getSuccesses(new_count + 1126, depth-1, path + "I")

# end #


import sys, time, traceback
sys.setrecursionlimit(1100)

# Typecast to sets in case the user tries '{}' to make an empty set
required_djinn, displayed_djinn = set(required_djinn), set(displayed_djinn)

try:
    print("Calculating...")
    init_time = time.time()
    Successes = []
    Checked = set()
    getSuccesses(INIT_COUNT, DEPTH)  # This does all the searching; updates Successes and Checked lists
    Successes = sorted(Successes, key=lambda x: x[2])  # Sorts the entries by g_count

    with open(OUTPUTFILE, "w") as f:  # Writes and formats data
        stat_names = ["HP", "PP", "ATK", "DEF", "AGI", "LCK"]
        for path, stats, g_count, djinn in Successes:
            f.write(path + ":\n")
            for name, stat_list in displayed_stats.items():
                for stat in stat_list:
                    f.write(f"  {name[:2]} {stat_names[stat]}: {stats[name][stat]},")
            f.write(f"\n  GRN: 0x{findValue(g_count):0>8X}  Gcount: {g_count}\n  Other: {djinn & displayed_djinn or ''}\n\n")

except Exception as e:
    print(traceback.format_exc())
else:
    print(f"""\
    Completed search at depth {DEPTH}
    Elapsed time: {time.time() - init_time}
    Outputted successfully to {OUTPUTFILE}""")
