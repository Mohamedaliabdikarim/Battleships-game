from random import randrange
import random

def validate_ship(boat, taken):
    boat.sort()
    for i in range(len(boat)):
        num = boat[i]
        if num in taken or num < 0 or num > 99:
            boat = [-1]
            break
        elif num % 10 == 9 and i < len(boat)-1 and boat[i+1] % 10 == 0:
            boat = [-1]
            break
        if i != 0 and boat[i] != boat[i-1]+1 and boat[i] != boat[i-1]+10:
            boat = [-1]
            break
    return boat

def get_random_ship(length, taken):
    valid_ship = False
    while not valid_ship:
        start_position = randrange(99)
        direction = randrange(1, 4)
        ship = validate_ship([start_position + i if direction == 2 else start_position - i * 10 for i in range(length)], taken)
        if ship[0] != -1:
            taken += ship
            valid_ship = True
    return ship, taken

def create_player_ships(taken, boats):
    player_ships = []
    for boat_length in boats:
        player_ship, taken = get_random_ship(boat_length, taken)
        player_ships.append(player_ship)
    return player_ships, taken

def validate_computer_ship(length, start, direction, taken):
    boat = []
    if direction == 1:
        boat = [start - i*10 for i in range(length)]
    elif direction == 2:
        boat = [start + i for i in range(length)]
    elif direction == 3:
        boat = [start + i*10 for i in range(length)]
    elif direction == 4:
        boat = [start - i for i in range(length)]
    boat = validate_ship(boat, taken)
    return boat

def create_computer_ships(taken, boats):
    computer_ships = []
    for length in boats:
        computer_ship = [-1]
        while computer_ship[0] == -1:
            start_position = randrange(99)
            direction = randrange(1, 4)
            computer_ship = validate_computer_ship(length, start_position, direction, taken)
        computer_ships.append(computer_ship)
        taken += computer_ship
    return computer_ships, taken

def display_player_board(taken):
    print("            Battleships    ")
    print("     0  1  2  3  4  5  6  7  8  9")

    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in taken:
                ch = " o "  
            row = row + ch
            place += 1
        print(x, " ", row)

def get_computer_shot(guesses, tactics):
    ok = "n"
    while ok == "n":
        try:
            if len(tactics) > 0:
                shot = tactics[0]
            else:
                shot = randrange(99)
            if shot not in guesses and 0 <= shot < 100:
                ok = "y"
                guesses.append(shot)
                break
        except:
            print("Incorrect entry - please enter again")
    return shot, guesses

def display_game_board(hit, miss, comp):
    print("            Battleships    ")
    print("     0  1  2  3  4  5  6  7  8  9")

    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in miss:
                ch = " x "
            elif place in hit:
                ch = " o "
            elif place in comp:
                ch = " O "  
            row = row + ch
            place += 1
        print(x, " ", row)

def check_player_shot(shot, computer_ships, hit, miss, comp):
    missed = 0
    for i in range(len(computer_ships)):      
        if shot in computer_ships[i]:
            computer_ships[i].remove(shot)
            if len(computer_ships[i]) > 0:
                hit.append(shot)
                missed = 1
            else:
                comp.append(shot)
                missed = 2                             
    if missed == 0:
        miss.append(shot)
    return computer_ships, hit, miss, comp, missed

def calculate_computer_tactics(shot, tactics, guesses, hit):
    temp = []
    if len(tactics) < 1:
        temp = [shot-1, shot+1, shot-10, shot+10]
    else:
        if shot-1 in hit:
            temp = [shot+1]
            for num in [2, 3, 4, 5, 6, 7, 8]:
                if shot-num not in hit:
                    temp.append(shot-num) 
                    break
        elif shot+1 in hit:
            temp = [shot-1]
            for num in [2, 3, 4, 5, 6, 7, 8]:
                if shot+num not in hit:
                    temp.append(shot+num) 
                    break
        if shot-10 in hit:
            temp = [shot+10]
            for num in [20, 30, 40, 50, 60, 70, 80]:
                if shot-num not in hit:
                    temp.append(shot-num) 
                    break
        elif shot+10 in hit:
            temp = [shot-10]
            for num in [20, 30, 40, 50, 60, 70, 80]:
                if shot+num not in hit:
                    temp.append(shot+num) 
                    break
    cand = []
    for i in range(len(temp)):
        if temp[i] not in guesses and temp[i] < 100 and temp[i] > -1:
            cand.append(temp[i])
    random.shuffle(cand)
    return cand

def get_player_shot(guesses):
    ok = "n"
    while ok == "n":
        try:
            shot = input("Please enter your guess: ")
            shot = int(shot)
            if shot < 0 or shot > 99:
                print("Incorrect number, please try again")
            elif shot in guesses:
                print("Incorrect number, used before")                
            else:
                ok = "y"
                break
        except:
            print("Incorrect entry - please enter again")
    return shot

def check_if_empty(list_of_lists):
    return all([not elem for elem in list_of_lists])

def play_battleship():
    print("Welcome to the Battleship game!")
    print("Your objective is to sink all the computer's ships before they sink yours.")
    print("On the game board, 'o' represents a hit, and 'x' represents a miss.")
    hit_player = []
    miss_player = []
    comp_player = []
    guesses_player = []  
    missed_player = 0
    tactics_player = []
    taken_player = []
    taken_computer = []
    hit_computer = []
    miss_computer = []
    comp_computer = []
    guesses_computer = []  
    missed_computer = 0
    tactics_computer = []
    
    battleships = [5, 4, 3, 3, 2, 2]

    # Computer creates a board for player 1
    ships_player, taken_player = create_player_ships(taken_player, battleships)

    # User creates the board for player 2 - show board
    ships_computer, taken_computer = create_computer_ships(taken_computer, battleships)
    display_player_board(taken_computer)

    print("Let the Battleship game begin!")

    # Loop
    for i in range(80):
        # Player shoots
        guesses_player = hit_player + miss_player + comp_player
        shot_player = get_player_shot(guesses_player)
        ships_player, hit_player, miss_player, comp_player, missed_player = check_player_shot(
            shot_player, ships_player, hit_player, miss_player, comp_player)
        display_game_board(hit_player, miss_player, comp_player)

        print("Your Hits:", hit_player)
        print("Your Misses:", miss_player)

        # Repeat until ships are empty
        if check_if_empty(ships_player):
            print("End of game - Winner in", i)
            break

        # Computer shoots
        shot_computer, guesses_computer = get_computer_shot(guesses_computer, tactics_computer)
        ships_computer, hit_computer, miss_computer, comp_computer, missed_computer = check_player_shot(
            shot_computer, ships_computer, hit_computer, miss_computer, comp_computer)
        display_game_board(hit_computer, miss_computer, comp_computer)

        print("Computer's Hits:", hit_computer)
        print("Computer's Misses:", miss_computer)

        # Update computer tactics
        if missed_computer == 1:
            tactics_computer = calculate_computer_tactics(
                shot_computer, tactics_computer, guesses_computer, hit_computer)
        elif missed_computer == 2:
            tactics_computer = []
        elif len(tactics_computer) > 0:
            tactics_computer.pop(0)

        # Check if computer ships are empty
        if check_if_empty(ships_computer):
            print("End of game - Computer wins in", i)
            break

play_battleship()

