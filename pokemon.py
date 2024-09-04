import random
import time
from tabulate import tabulate

def display_pokemon_options(pokemon_dict):
    print("                                         Select your Pokemon Character Here!!!\n                                                   ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓")
    for key, value in pokemon_dict.items():
        print(f"                                        Pokemon: {key:<10} ---  Base Power: {value}")
    print()

def choose_pokemon(pokemon_dict):
    while True:
        chosen_pokemon = input("Which pokemon would you like to choose: ").capitalize()
        if chosen_pokemon in pokemon_dict:
            return chosen_pokemon
        else:
            print("Invalid input, please choose a valid Pokemon.")
            continue

def calculate_power(base_power, category):
    if category == "Weak":
        additional_power = random.randint(50, 100)
    elif category == "Average":
        additional_power = random.randint(101, 150)
    else:  # Strong
        additional_power = random.randint(151, 200)
    current_power = base_power + additional_power
    return additional_power, current_power

def determine_category_and_calculate(pokemon_dict, chosen_pokemon):
    categories = ["Weak", "Average", "Strong"]
    random_category = random.choice(categories)

    base_power = pokemon_dict[chosen_pokemon]
    additional_power, current_power = calculate_power(base_power, random_category)

    return random_category, additional_power, current_power

def random_enemy(pokemon_dict):
    random_player = random.randint(100, 1000)
    print("                                                  Calculating Power...                   ")
    time.sleep(3)
    print("                                                  Finding Enemy...")
    time.sleep(3)
    print(
        f"---------------------------------------------- Enemy Found (Player_{random_player}) ----------------------------------------------")

    enemy_pokemon = random.choice(list(pokemon_dict.keys()))
    enemy_base_power = pokemon_dict[enemy_pokemon]

    enemy_categories = ["Weak", "Average", "Strong"]
    enemy_category = random.choice(enemy_categories)

    additional_power, current_power = calculate_power(enemy_base_power, enemy_category)

    return {
        'pokemon': enemy_pokemon,
        'category': enemy_category,
        'additional_power': additional_power,
        'current_power': current_power
    }

def main():
    player_pokemon = {
        "Pikachu": 50,
        "Charmander": 55,
        "Bulbasaur": 60,
        "Squirtle": 58,
        "Jigglypuff": 45,
        "Eeve": 52,
        "Snorlax": 80,
        "Gengar": 70,
        "Machamp": 75,
        "Mewtwo": 90,
    }

    computer_pokemon = {
        "Pikachu": 50,
        "Charmander": 55,
        "Bulbasaur": 60,
        "Squirtle": 58,
        "Jigglypuff": 45,
        "Eeve": 52,
        "Snorlax": 80,
        "Gengar": 70,
        "Machamp": 75,
        "Mewtwo": 90,
    }

    chosen_pokemon = None
    enemy = None  # Dictionary to store enemy details

    user_wins = 0
    computer_wins = 0

    battle_number = 1
    battle_summary = []

    pokemon_change_limit = 5
    pokemon_changes = 0
    max_battles = 5

    while battle_number <= max_battles:
        if chosen_pokemon is None:
            display_pokemon_options(player_pokemon)
            chosen_pokemon = choose_pokemon(player_pokemon)

        # Find the enemy after the player has chosen their pokemon
        enemy = random_enemy(computer_pokemon)

        # Determine power for the current pokemon
        pokemon_category, pokemon_additional_power, pokemon_current_power = determine_category_and_calculate(
            player_pokemon, chosen_pokemon)

        print("                                                   Battle Time!")
        time.sleep(1)
        print("                                                         3")
        time.sleep(1)
        print("                                                         2")
        time.sleep(1)
        print("                                                         1")
        time.sleep(1)

        # Print battle details
        print(f"Your Pokemon: {chosen_pokemon} ({pokemon_category})")
        print(f"Base Power: {player_pokemon[chosen_pokemon]}")
        print(f"Additional Power: {pokemon_additional_power}")
        print(f"Current Power: {pokemon_current_power}")
        print()
        print("                                                         V.S")
        print()
        print(f"Enemy Pokemon: {enemy['pokemon']} ({enemy['category']})")
        print(f"Base Power: {computer_pokemon[enemy['pokemon']]}")
        print(f"Additional Power: {enemy['additional_power']}")
        print(f"Current Power: {enemy['current_power']}")

        # Compare powers and determine the outcome
        if pokemon_current_power > enemy['current_power']:
            print("                                                      You Win!")
            # Update the base power of the winning pokemon
            player_pokemon[chosen_pokemon] += enemy['current_power']
            user_wins += 1
            result = "User Wins"
        elif pokemon_current_power < enemy['current_power']:
            print("                                                      You Lose!")
            # Update the base power of the losing pokemon and the enemy
            if player_pokemon[chosen_pokemon] > enemy['current_power']:
                player_pokemon[chosen_pokemon] -= enemy['current_power']
            else:
                player_pokemon[chosen_pokemon] = 0
            computer_pokemon[enemy['pokemon']] += pokemon_current_power
            computer_wins += 1
            # Change computer's pokemon if it lost
            result = "Computer Wins"
        else:
            print("                                                    It's a tie.")
            result = "Tie"

        print(f"Updated {chosen_pokemon}'s Base Power: {player_pokemon[chosen_pokemon]}")

        # Add battle details to summary
        battle_summary.append({
            'battle_number': battle_number,
            'user_power': pokemon_current_power,
            'enemy_power': enemy['current_power'],
            'status': result
        })
        battle_number += 1

        # Prompt user for next action
        while True:
            print(
                "Do you want to continue battling? (Press 'c' to continue with the same pokemon, 'n' to choose a new pokemon, 'x' to exit)")
            choice = input("---->").lower()

            if choice == 'x':
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Thank you for playing!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("\nOverall Winner: " + (
                    'User' if user_wins > computer_wins else 'Computer' if computer_wins > user_wins else 'No One (Tie)'))
                print(f"Total Battles: {battle_number - 1}")
                print(f"User Wins: {user_wins}")
                print(f"Computer Wins: {computer_wins}")

                # Display battle summary using tabulate
                print("\nBattle Summary:")
                table_data = [
                    [battle['battle_number'], battle['user_power'], battle['enemy_power'], battle['status']]
                    for battle in battle_summary
                ]
                headers = ["Battle Number", "User Power", "Enemy Power", "Status"]
                print(tabulate(table_data, headers, tablefmt="grid"))

                return
            elif choice == 'n':
                if pokemon_changes < pokemon_change_limit:
                    # Reset chosen pokemon and find a new enemy
                    chosen_pokemon = None  # Reset chosen pokemon to allow new selection
                    pokemon_changes += 1
                    break
                else:
                    print(f"You have reached the limit of {pokemon_change_limit} pokemon changes.")
                    break
            elif choice == 'c':
                # Keep the current enemy and pokemon
                break
            else:
                print("Invalid input. Please enter 'c', 'n', or 'x'.")

    # End of game message
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Thank you for playing!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\nOverall Winner: " + (
        'User' if user_wins > computer_wins else 'Computer' if computer_wins > user_wins else 'No One (Tie)'))
    print(f"Total Battles: {max_battles}")
    print(f"User Wins: {user_wins}")
    print(f"Computer Wins: {computer_wins}")

    # Display battle summary using tabulate
    print("\nBattle Summary:")
    table_data = [
        [battle['battle_number'], battle['user_power'], battle['enemy_power'], battle['status']]
        for battle in battle_summary
    ]
    headers = ["Battle Number", "User Power", "Enemy Power", "Status"]
    print(tabulate(table_data, headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
