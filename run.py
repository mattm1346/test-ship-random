from random import randrange
import random

print(
    '''  ____       _______ _______ _      ______  _____ _    _ _____ _____   _____ 
|  _ \   /\|__   __|__   __| |    |  ____|/ ____| |  | |_   _|  __ \ / ____|
| |_) | /  \  | |     | |  | |    | |__  | (___ | |__| | | | | |__) | (___  
|  _ < / /\ \ | |     | |  | |    |  __|  \___ \|  __  | | | |  ___/ \___ \ 
| |_) / ____ \| |     | |  | |____| |____ ____) | |  | |_| |_| |     ____) |
|____/_/    \_\_|     |_|  |______|______|_____/|_|  |_|_____|_|    |_____/ 
''')
# http://www.network-science.de/ascii/
# https://www.asciiart.eu/


def check_board(b, taken):
    b.sort()
    for i in range(len(b)):
        num = b[i]
        # Check for duplicates so ships do not overlap
        if num in taken:
            b = [-1]
            break
        elif num < 0 or num > 99:
            b = [-1]
            break
        # Add statement if number ends in 9 then continues
        # If ends in 0 then not valid
        elif b[i] % 10 == 9 and i < len(b) - 1:
            if b[i+1] % 10 == 0:
                b = [-1]
                break
        if i != 0:
            if b[i] != b[i-1]+1 and b[i] != b[i-1]+10:
                b = [-1]
                break

    return b


def get_ship(long, taken):
    loop = True
    while loop:
        ship = []
        # user input numbers
        print('enter ship of length', long)
        for i in range(long):
            boat_num = input('Please enter a number ')
            ship.append(int(boat_num))
        # check ship
        ship = check_board(ship, taken)
        if ship[0] != -1:
            taken = taken + ship
            break
        else:
            print('error, try again')
    return ship


def create_ships_player():
    taken = []
    ships = []
    boats = [5, 4, 3, 3, 2, 2]

    for boat in boats:
        ship = get_ship(boat, taken)
        ships.append(ship)
    return ships


ships = create_ships_player()


def check_boat(boat, start, direct, taken):
    b = []
    # up
    if direct == 1:
        for i in range(boat):
            b.append(start - i * 10)
            b = check_board(b, taken)
    # right
    elif direct == 2:
        for i in range(boat):
            b.append(start + i)
            b = check_board(b, taken)
    # down
    elif direct == 3:
        for i in range(boat):
            b.append(start + i * 10)
            b = check_board(b, taken)
    # left
    elif direct == 4:
        for i in range(boat):
            b.append(start - i)
            b = check_board(b, taken)
    return(b)


def create_ships():
    taken = []
    ships = []
    boats = [5, 4, 3, 3, 2, 2]
    for boat in boats:
        b = [-1]
        while b[0] == -1:
            boat_start = randrange(99)
            # boat_direct - 1 = up, 2 = right, 3 = down, 4 = left
            boat_direct = randrange(1, 4)
            # print(boat, boat_start, boat_direct)
            b = check_boat(boat, boat_start, boat_direct, taken)
        ships.append(b)
        taken = taken + b
        # print(ships)
    return ships, taken


# Create function to show board
def show_board_c(taken):
    print('   0 1 2 3 4 5 6 7 8 9')
    # Create loop for board
    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            character = " _"
            if place in taken:
                character = " o"
            row = row + character
            place = place + 1
        print(x, row)


# Add input for user guess
def guess_comp(guesses, tactics):
    # Create while loop so guess will run until input is valid
    loop = 'no'
    while loop == 'no':
        if len(tactics) > 0:
            shot = tactics[0]
        else:
            shot = randrange(99)
        if shot not in guesses:
            loop = 'yes'
            guesses.append(shot)
            break
    return shot, guesses


def show_board(hit, miss, sink):
    print('   0 1 2 3 4 5 6 7 8 9')
    # Create loop for board
    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            character = " _"
            if place in miss:
                character = " x"
            elif place in hit:
                character = " o"
            elif place in sink:
                character = " O"
            row = row + character
            place = place + 1
        print(x, row)


def check_shot(shot, boats, hit, miss, sink):
    missed = 0
    for i in range(len(boats)):
        if shot in boats[i]:
            boats[i].remove(shot)
            if len(boats[i]) > 0:
                hit.append(shot)
                missed = 1
            else:
                sink.append(shot)
                missed = 2
    # If shot misses, place in list
    if missed == 0:
        miss.append(shot)

    return boats, hit, miss, sink, missed


def calc_tactics(shot, tactics, guesses, hit):
    temp = []
    if len(tactics) < 1:
        temp = [shot-1, shot+1, shot-10, shot+10]
    else:
        if shot - 1 in hit:
            if shot - 2 in hit:
                temp = [shot-3, shot+1]
            else:
                temp = [shot-2, shot+1]
        elif shot + 1 in hit:
            if shot - 2 in hit:
                temp = [shot+3, shot-1]
            else:
                temp = [shot+2, shot-1]
        elif shot - 10 in hit:
            if shot - 2 in hit:
                temp = [shot-30, shot+10]
            else:
                temp = [shot-20, shot+10]
        elif shot + 10 in hit:
            if shot - 2 in hit:
                temp = [shot+30, shot-10]
            else:
                temp = [shot+20, shot-10]
    cand = []
    for i in range(len(temp)):
        if temp[i] not in guesses and temp[i] < 100 and temp[i] > -1:
            cand.append(temp[i])
    random.shuffle(cand)
    return cand


def check_if_empty(list_of_lists):
    return all([not elem for elem in list_of_lists])


hit = []
miss = []
sink = []
guesses = []
boats, taken = create_ships()
tactics = []
for i in range(80):
    shot, guesses = guess_comp(guesses, tactics)
    boats, hit, miss, sink, missed = check_shot(shot, boats, hit, miss, sink)
    if missed == 1:
        tactics = calc_tactics(shot, tactics, guesses, hit)
    elif missed == 2:
        tactics = []
    elif len(tactics) > 0:
        tactics.pop(0)

    if check_if_empty(boats):
        print('Game Finished', i)
        break

show_board_c(taken)
show_board(hit, miss, sink)
