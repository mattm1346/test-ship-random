from random import randrange

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

    return b


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
def guess_comp(guesses):
    # Create while loop so guess will run until input is valid
    loop = 'no'
    while loop == 'no':
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
    missed = 1
    for i in range(len(boats)):
        if shot in boats[i]:
            boats[i].remove(shot)
            missed = 0
            if len(boats[i]) > 0:
                hit.append(shot)
            else:
                sink.append(shot)
    # If shot misses, place in list
    if missed == 1:
        miss.append(shot)

    return boats, hit, miss, sink


hit = []
miss = []
sink = []
guesses = []
boats, taken = create_ships()
show_board_c(taken)
for i in range(50):
    shot, guesses = guess_comp(guesses)
    boats, hit, miss, sink = check_shot(shot, boats, hit, miss, sink)
    show_board(hit, miss, sink)
