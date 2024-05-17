import os
import time

# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2},
    "Super Mario Bros": {"quantity": 5, "cost": 3},
    "Tetris": {"quantity": 5, "cost": 1},
    "Pacman": {"quantity": 3, "cost": 2}}
# Dictionary to store user accounts with their balances and points
user_accounts = {}
# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("=============================================================================================")
    print("List of Available Games:")
    print("=============================================================================================")
    for games, details in game_library.items():
        print(f"{games}: {details['quantity']} units available. Rental cost = ${details['cost']}") 

# Function to register a new user
def register_user():
    global user_accounts
    print("=============================================================================================")
    print("Register User")
    print("=============================================================================================")
    username = input("Enter a new username: ")
    if username in user_accounts.keys():
        print("Username already taken. Please try again.")
    if username == "":
        return
    else:
        password = input("Enter a new password (minimum of 8 characters): ")
        if len(password) < 8:
            print("Please enter a password with a minimum of 8 characters.")
        if password == "":
            return
        else:
            user_accounts[username] = {"password": password, "balance": 0, "points": 0, "inventory": {}}
            print("Account successfully created.")
            time.sleep(1)            
            os.system('cls')
            return

# Function to rent a game
def rent_game(username):
    if user_accounts[username]["balance"] == 0:
        print("=============================================================================================")
        print("The current balance of your account is 0. Please top up your balance first before renting a game.")
        print("=============================================================================================")
        input("Press ENTER to go back to MENU.")
        return
    while True:
        try:
            print("=============================================================================================")
            print("Hello,", username)
            print("=============================================================================================")
            display_available_games()
            print("=============================================================================================")
            print("\nBalance: ", user_accounts[username]["balance"])
            print("=============================================================================================")
            game_num = input("Enter a game to rent (number only): ")
            if game_num == "":
                return
            game_num = int(game_num)
            if 1 <= game_num <= len(game_library):
                game = list(game_library.keys())[game_num - 1]
                if game_library[game]["quantity"] > 0:
                    quantity = int(input(f"Enter how many copy/s of {game} to rent: "))
                    if 1 <= quantity <= game_library[game]["quantity"]:
                        os.system('cls')
                        print("=============================================================================================")
                        print(f"Rented {quantity} copy/s of {game}.")
                        game_library[game]["quantity"] -= quantity
                        if game in user_accounts[username]["inventory"]:
                            user_accounts[username]["inventory"][game]["copy/ies"] += quantity
                        else:
                            user_accounts[username]["inventory"][game] = {"copy/ies": quantity}
                            cost = quantity * game_library[game]["cost"]
                            cost = (cost)
                            balance = user_accounts[username]["balance"] - cost
                            points = cost / 2
                            user_accounts[username]["balance"] = balance
                            user_accounts[username]["points"] += int(points)
                            if game_library[game]["quantity"] == 0:
                                del game_library[game]
                            print(f"Total cost to rent {quantity} copy/s of {game} is {cost}.")
                            print(f"{cost} deducted from balance.")
                            print(f"{int(points)} points earned from renting.")
                            time.sleep(1)
                            print("=============================================================================================")
                            display_inventory(username)
                            print(f"\nBalance: {user_accounts[username]["balance"]}\nPoints: {user_accounts[username]["points"]}")
                            print("=============================================================================================")
                            input("\nPress Enter to continue.")
                            break
                    else:
                        print(f"There are only {game_library[game]['quantity']} copy/ies of {game}.")
                        input("\nPress Enter to continue...")
            else:
                print(f"Choose from 1 to {len(game_library)} only.")
                input("\nPress Enter to continue...")
                os.system('cls')
        except ValueError:
            print(f"Please enter a positive integer only.")
            input("\nPress Enter to continue...")
            os.system('cls')

# Function to return a game
def return_game(username):
    if not user_accounts[username]["inventory"]:
        print("You don't have anything in your inventory to return.")
        input("Press Enter to go to MENU...")
        return
    else:
        while True:
            try:
                display_inventory(username)
                print("=============================================================================================")
                game_num = input("Enter the number of the game you want to return: ")
                if game_num == "":
                    return
                game_num = int(game_num)
                inventory = user_accounts[username]["inventory"]

                if 1 <= game_num <= len(inventory):
                    game = list(inventory.keys())[game_num - 1]
                    quantity = input(f"Enter the number of {game} copies to return: ")
                    if quantity == "":
                        return
                    quantity = int(quantity)
                    if quantity <= 0:
                        print("Please enter a positive value.")
                        return
                    if quantity  > inventory [game]["copy/ies"]:
                        print("You don't have that much copies to return.")
                        return
                    inventory[game]["copy/ies"] -= quantity
                    game_library[game]["quantity"] += quantity

                    if inventory[game]["copy/ies"] == 0:
                        del user_accounts[username]["inventory"][game]
                        os.system('cls')
                        print("=============================================================================================")
                        print(f"All copies of the {game} was returned and removed from inventory.")
                    else:
                        print(f"{quantity} copy/ies of {game} returned.")
                        print("=============================================================================================")
                    time.sleep(0.5)
                    display_inventory(username)
                else:
                    print(f"Invalid game number. Please choose from 1 to {len(inventory)}.")
                    input("Press Enter to continue...")
                    break
            except ValueError:
                print("Please only enter a positive integer.")
                os.system('cls')

# Function to top-up user account
def top_up_account(username):
    print("=============================================================================================")
    print("TOP UP YOUR BALANCE")
    print(f"\nCurrent Balance: ${user_accounts[username]["balance"]}")
    print("=============================================================================================")
    while True:
        try:
            input_amount = input("Enter the amount you want to add in your balance: ")
            if input_amount == "":
                return
            amount = float(input_amount)
            if amount <= 0:
                print("Please only enter a positive number.")
                input("Press enter to continue...")
                os.system('cls')
            else:
                print("=============================================================================================")
                user_accounts[username]["balance"] += amount
                print("New balance successfully updated!")
                print(f"Balance: ${user_accounts[username]["balance"]}")
                print("=============================================================================================")
                input("Press enter to continue...")
                os.system('cls')
                break
        except ValueError:
            print("Please only enter a positive integer.")
            os.system('cls')

# Function to display user's inventory
def display_inventory(username):
    inventory = user_accounts[username]["inventory"]
    if not inventory:
        print("=============================================================================================")
        print("Your inventory is empty. :(")
        print("=============================================================================================")
    else:
        print("=============================================================================================")
        print(f"{username}'s inventory")
        n = 1
        for game, details in inventory.items():
            print(f"{n}. {game}")
            print(f"Quantity: {details['copy/ies']} piece/s")
            n += 1
        print("=============================================================================================")
    input("Press Enter to continue...")
    os.system('cls')
        
# Function for admin to update game details
def admin_update_game():
    while True:
        try:
            display_available_games()
            print("============================================================================================================================================================================")
            print("1. Update Game Details")
            print("2. Add Game")
            print("3. Remove Game")
            choice = input("Enter your choice: ")
            if choice == "":
                break
            choice = int(choice)
            if choice == 1:
                os.system('cls')
                print("============================================================================================================================================================================")
                while True:
                    n = 1
                    for game in (game_library.keys()):
                        print(f"{n}. {game}")
                        n += 1
                    game_num = input("Choose to edit a game (Number only): ")
                    if game_num == "":
                        return
                    game_num = int(game_num)
                    if 1 <= game_num <= len(game_library.keys()):
                        game = list(game_library.keys())[game_num - 1]
                        while True:
                            os.system('cls')
                            print("============================================================================================================================================================================")
                            print("1. Name Change")
                            print("2. Quantity Change")
                            print("3. Price Change")
                            print("============================================================================================================================================================================")
                            option = input("Choose option: ")
                            if option == "":
                                return
                            option = int(option)
                            if option == 1:
                                name_game = input(f"Enter new name for {game}: ")
                                if name_game == "":
                                    return
                                if name_game in game_library:
                                    print("Name already exists in the game library.")
                                else:
                                    game_details = game_library.pop(game)
                                    game_library[name_game.title()] = game_details
                                    print(f"{game} has changed into {name_game}.\n")
                                    time.sleep(0.5)
                                    os.system('cls')
                                    print("============================================================================================================================================================================")
                            elif option == 2:
                                new_stocks = input(f"Enter new stocks for {game}: ")
                                if new_stocks == "":
                                    return
                                else:
                                    new_stocks = int(new_stocks)
                                    game_library[game]["quantity"] = new_stocks
                                    print(f"Quantity of the {game} has been changed to {new_stocks}. \n")
                                    time.sleep(0.5)
                                    os.system('cls')
                                    print("============================================================================================================================================================================")
                            elif option == 3:
                                new_price = input(f"Enter new price for {game}: ")
                                if new_price == "":
                                    return
                                else:
                                    new_price = int(new_price)
                                    game_library[game]["cost"] = new_price
                                    print(f"Price for the {game} has been changed to {new_price}.\n")
                                    time.sleep(0.5)
                                    os.system('cls')
                                    print("============================================================================================================================================================================")
                            else:
                                print("Only choose 1-3.")
                                input("\nPress Enter to continue.")
                                os.system('cls')
                    else: 
                        print(f"Choose from 1 to {len(game_library.keys())} only. ")
                        input("\nPress Enter to continue...")
                        os.system('cls')
            elif choice == 2:
                os.system('cls')
                print("============================================================================================================================================================================")
                add_game = input("Enter the name of the game you want to add: ")
                if add_game == "":
                    return
                if add_game not in game_library.keys():
                    quantity = input("Enter the quantity of the game: ")
                    if quantity == "":
                        return
                    quantity = int(quantity)
                    if quantity > 0:
                        cost = input(f"Enter price per copy of {add_game}: ")
                        if cost == "":
                            return
                        cost = int(cost)
                        if cost >= 1:
                            game_library[add_game] = {"quantity": quantity, "cost": cost}
                            print(f"{add_game} has been added to library.")
                            time.sleep(0.5)
                            os.system('cls')
                            print("============================================================================================================================================================================")
                        else:
                            print("Enter a positive number")
                            print("\nPlease Enter to continue...")
                    else:
                        print("Enter a positive number")
                        print("\nPlease Enter to continue...")
                else:
                    print("This is already in the game library.")
                    print("\nPlease Enter to continue...")
            elif choice == 3:
                while True:
                    os.system('cls')
                    print("============================================================================================================================================================================")
                    n = 1
                    for game in (game_library.keys()):
                        print(f"{n}. {game}")
                        n += 1
                    game_rem = input("Enter the game you want to remove: ")
                    if game_rem == "":
                        return
                    game_rem = int(game_rem)
                    if 1 <= game_rem <= len (game_library.keys()):
                        game = list(game_library.keys())[game_rem - 1]
                        del game_library[game]
                        print(f"The {game} was removed from the library.")
                        time.sleep(0.5)
                        os.system('cls')
                        print("============================================================================================================================================================================")
                    else:
                        print(f"Choose from 1 to {len(game_library.keys())} only. ")
                        input("\nPress Enter to continue...")
                        os.system('cls')
            else:
                print("Only choose 1-3.")
                input("\nPress Enter to continue.")
                os.system('cls')
        except ValueError:
            print("Please enter a positive integer only.")
            time.sleep(1)
            os.system('cls')

# Function for admin login
def admin_login():
    print("ADMIN USER")
    print("=============================================================================================")
    username = input("Enter username: ")
    password = input("Enter password: ")
    print("=============================================================================================")
    if username != "admin":
        print("Incorrect username.")
        time.sleep(1)            
        os.system('cls')
        return
    elif password != "adminpass":
        print("Incorrect password.")
        time.sleep(1)            
        os.system('cls')
    else:
        os.system('cls')
        admin_menu()

# Admin menu
def admin_menu():
    while True:
        try:
            print("ADMIN MENU")
            print(f"Welcome back, {admin_username}!")
            print("=============================================================================================")
            print("1. Update/Change Game Details")
            print("2. Game Inventory")
            print("3. Log Out")
            print("=============================================================================================")
            option = int(input("Choose option: "))
            if option == 1:
                os.system('cls')
                admin_update_game()
            elif option == 2:
                os.system('cls')
                display_game_inventory()
            elif option == 3:
                os.system('cls')
                exit = "\nExiting program..."
                for char in exit:
                    print(char, end="")
                    time.sleep(1)  
                break          
            else:
                print("Choose only from 1-4.")
                time.sleep(1)
        except ValueError:
            print("Please enter a positive integer only.")
            time.sleep(1)
            
# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    if user_accounts[username]["points"] < 3:
        print("Your balance is insufficient to redeem a free rental game. At least 3 points are needed.")
        input("\nPress Enter to go back to menu...")
    else:
        print("==================================================================================================================================================================================")
        print("Game Library:")
        n = 1
        for game in (game_library.keys()):
            print(f"{n}. {game}")
            n += 1
        print(f"{username}'s points: ", user_accounts[username]["points"])
        choice = input("Choose a game to redeem with points: ")
        if choice == "":
            return
        else:
            choice = int(choice)
            game = list(game_library.keys())[choice - 1]
            if game in user_accounts[username]["inventory"]:
                user_accounts[username]["inventory"][game]["copy/ies"] += 1
            else:
                user_accounts[username]["inventory"][game] = {"copy/ies": 1}
                user_accounts[username]["points"] -= 3
                time.sleep(0.3)
                os.system('cls')
                print("==================================================================================================================================================================================")
                print(f"{game} redeemed successfully! This will be added in your inventory. Enjoy!")
                print(f"3 points were deducted")
                time.sleep(0.2)
                print("==================================================================================================================================================================================")
                display_inventory(username)
                print(f"Remaining Balance: {user_accounts[username]["balance"]}\n Remaining points: {user_accounts[username]["points"]}")
                print("==================================================================================================================================================================================")
                input("Press Enter to go back to menu...")

# Function to display game inventory
def display_game_inventory():
    display_available_games()
    for username, details in user_accounts.items():
        games_rented = details["inventory"]
        if games_rented:
            print("============================================================================================================================================================================")
            print("Rented Games:")
            print(f"{username}: ")
            for game, quantity in games_rented.items():
                print(f"{game}, Quantity: {quantity}")
            print("============================================================================================================================================================================")
        else:
            print("You don't have any rented games.")
            input("Press Enter to go to MENU...")

# Function to handle user's logged-in menu
def logged_in_menu(username):
    while True:
        try:
            print("============================================================================================================================================================================")
            print("GAME RENTAL")
            print("============================================================================================================================================================================")
            print(f"Welcome, {username}!")
            print("1. Rent/Return Game")
            print("2. Check Inventory")
            print("3. Top Up Balance")
            print("4. Log Out")
            print("============================================================================================================================================================================")
            choice = int(input("Choose a number: "))
            if choice == 1:
                os.system('cls')
                while True:
                    try:
                        print("============================================================================================================================================================================")
                        print([display_available_games()])
                        print("============================================================================================================================================================================")
                        print("1. Rent Game")
                        print("2. Redeem Free Rental")
                        print("3. Return Game")
                        option = input("Enter your choice (Press ENTER to exit): ")
                        print("============================================================================================================================================================================")
                        if option == "":
                            break
                        option = int(option)
                        if option == 1:
                            os.system('cls')
                            rent_game(username)
                        elif option == 2:
                            os.system('cls')
                            redeem_free_rental(username)
                        elif option == 3:
                            os.system('cls')
                            return_game(username)
                        else:
                            print("Only choose from 1-3.")
                            time.sleep(1)
                    except ValueError:
                        print("Please only enter a positive integer.")
                        time.sleep(1)
            elif choice == 2:
                os.system('cls')
                display_inventory()
            elif choice == 3:
                os.system('cls')
                top_up_account(username)
            elif choice == 4:
                os.system('cls')
                exit = "\nExiting program..."
                for char in exit:
                    print(char, end="")
                    time.sleep(1)  
                break          
            else:
                print("Choose only from 1-4.")
                time.sleep(1)
        except ValueError:
            print("Please enter a positive integer only.")
            time.sleep(1)
            os.system('cls')
# Function to check user credentials
def check_credentials( ):
    if not user_accounts:
        print("Unable to login. The account is not registered.")
        input("Press Enter to go back to MENU...")
    else:
        print("LOGIN USER")
        print("==================================================================================================================================================================================")
        while True:
            username = input("Enter username: ")
            if username == "":
                break
            if username not in user_accounts.keys():
                print("Username not found. Please enter a registered username.")
                time.sleep(1)
            else:
                while True:
                    password = input(f"Enter password for {username} (Press ENTER to exit): ")
                    if password == "":
                        break
                    if password == user_accounts[username]["password"]:
                        print("Login Successful!")
                        time.sleep(0.5)
                        os.system('cls')
                        logged_in_menu(username)
                    else:
                        print("Password is not correct.")
                        time.sleep(0.5)
                        
# Main function to run the program
def main():
    while True:
        try:
            print("============================================================================================================================================================================")
            print("Welcome to Game Rental!")
            print("============================================================================================================================================================================")
            print("1. Login")
            print("2. Register")
            print("3. Admin Login")
            print("4. Exit")
            print("============================================================================================================================================================================")
            choice = int(input("Enter choice: "))
            if choice == 1:
                os.system('cls')
                check_credentials()
            elif choice == 2:
                os.system('cls')
                register_user()
            elif choice == 3:
                os.system('cls')
                admin_login()
            elif choice == 4:
                os.system('cls')
                exit = "\nExiting program..."
                for char in exit:
                    print(char, end="")
                    time.sleep(0.5)
                break  
            else:
                print("Choose only fro 1-4.")
        except ValueError:
            print("Please enter a positive integer.")
            os.system('cls')
            time.sleep(0.5)

if __name__ == "__main__":
    main()