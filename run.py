from random import randrange, shuffle

def is_valid_ship(boat, taken):
    boat.sort()
    for i in range(len(boat)):
        num = boat[i]
        if num in taken or not (0 <= num <= 99):
            return False
        elif num % 10 == 9 and i < len(boat) - 1:
            if boat[i + 1] % 10 == 0:
                return False
        if i != 0 and (boat[i] != boat[i - 1] + 1 and boat[i] != boat[i - 1] + 10):
            return False
    return True

def get_user_ship(length, taken):
    while True:
        ship = []
        print(f"Enter your ship of length {length}:")
        for _ in range(length):
            try:
                boat_num = int(input("Please enter a number: "))
                ship.append(boat_num)
            except ValueError:
                print("Invalid input. Please enter a number.")
                break

        if is_valid_ship(ship, taken):
            taken.extend(ship)
            return ship, taken
        else:
            print("Error - please try again")

def create_user_ships(boats):
    ships = []
    taken = []
    for boat in boats:
        ship, taken = get_user_ship(boat, taken)
        ships.append(ship)
    return ships, taken

def create_computer_ships(boats):
    ships = []
    taken = []
    for length in boats:
        ship = [-1]
        while ship[0] == -1:
            boat_start = randrange(99)
            boat_direction = randrange(1, 4)
            ship = check_boat(length, boat_start, boat_direction, taken)
        ships.append(ship)
        taken.extend(ship)
    return ships, taken

def show_board_c(taken):
    print("            Battleships    ")
    print("     0  1  2  3  4  5  6  7  8  9")

    place = 0
    for x in range(10):
        row = ""
        for _ in range(10):
            ch = " _ "
            if place in taken:
                ch = " o "
            row += ch
            place += 1
        print(x, " ", row)

def get_comp_shot(guesses, tactics):
    while True:
        if tactics:
            shot = tactics[0]
        else:
            shot = randrange(99)
        if shot not in guesses:
            guesses.append(shot)
            return shot, guesses

def show_board(hit, miss, comp):
    print("            Battleships    ")
    print("     0  1  2  3  4  5  6  7  8  9")

    place = 0
    for x in range(10):
        row = ""
        for _ in range(10):
            ch = " _ "
            if place in miss:
                ch = " x "
            elif place in hit:
                ch = " o "
            elif place in comp:
                ch = " O "
            row += ch
            place += 1
        print(x, " ", row)

def check_shot(shot, ships, hit, miss, comp):
    missed = 0
    for i in range(len(ships)):
        if shot in ships[i]:
            ships[i].remove(shot)
            if len(ships[i]) > 0:
                hit.append(shot)
                missed = 1
            else:
                comp.append(shot)
                missed = 2
    if missed == 0:
        miss.append(shot)
    return ships, hit, miss, comp, missed

def calc_tactics(shot, tactics, guesses, hit):
    temp = []
    if len(tactics) < 1:
        temp = [shot - 1, shot + 1, shot - 10, shot + 10]
    else:
        if shot - 1 in hit:
            temp = [shot + 1]
            for num in range(2, 9):
                if shot - num not in hit:
                    temp.append(shot - num)
                    break
        elif shot + 1 in hit:
            temp = [shot - 1]
            for num in range(2, 9):
                if shot + num not in hit:
                    temp.append(shot + num)
                    break
        if shot - 10 in hit:
            temp = [shot + 10]
            for num in range(20, 80, 10):
                if shot - num not in hit:
                    temp.append(shot - num)
                    break
