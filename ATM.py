import mysql.connector
import logging
from User import User
from datetime import datetime

# GLOBAL CREATION
global mydb
global mycursor
global current_user
global current_pin
global current_id
global user

#SETUP LOGGING
logging.basicConfig(filename='errors.log', encoding='utf-8', level=logging.DEBUG)

#DATABASE CONNECTION
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sqlProject0",
    database = "demodatabase"
)

mycursor = mydb.cursor()

#INITIALIZE OUR VARIABLES
current_user = ''
current_pin = 0
current_id = 0
result = 0


def create_account():
    """
    This function will allow a user to create a new account if they enter the word 'New'.
    We will receive two inputs:
        requested_username: The username that the guest wants to login as
        requested_pin: The pin the user wants to set to protect account.
    No parameters or return values.
    """

    print("""  _________________________________________
    //       Let's create an account!          \\
    =============================================
    """)

    #Get Username
    print("Please enter your desired username: ")
    requested_username = ''
    requested_username = str(input())

    #Get Pin
    print("You will need a four digit PIN.")
    print("Please enter your desired PIN: ")
    requested_pin = -1

    while (requested_pin < 0):
        try: 
            requested_pin = int(input())
            logging.error("If you pressed enter then without any input then you probably got this error")
        except ValueError:
            print("Invalid input. Try again.")

    #Create initial login details into our login database
    sql = "INSERT INTO `userlogins`(userName,userPin) VALUES (%s, %s)"
    val = (requested_username, requested_pin)
    mycursor.execute(sql, val)
    mydb.commit()

    #Get the new ID created from database (Incremented Automically in SQL)
    mycursor.execute(f"SELECT id FROM userlogins WHERE userName=('{requested_username}')")
    myresult = mycursor.fetchall()
    for row in myresult:
        result = row[0]
    new_id = result

    #Create the beginning bank information/data in our database.
    sql = "INSERT INTO `userdata`(user_id,balance) VALUES (%s, %s)"
    val = (new_id, 5000)
    mycursor.execute(sql, val)
    mydb.commit()

    print("New account created! Taking you back to the login!")


def open_login():
    """
    Initial start of the app. It authenticates the username and password or gives the option for a user to create a new account.
    Once they get a correct pairing of Username and Pairing we will open the menu.

    Returns:
        * Returns a tuple of important information about the account we are interacting with.
        current_user: The current username that is signed in.'
        current_pin: The current pin that is signed in.
        current_id: The current ID of the account signed in.
        user: The User that we've created and will be using to interact with that specific user's bank account.
    """

    #Open Login Dialog
    print("""       _______________________________________
    //       Welcome to Revature Banking       \\\\
    || If you need to register for a new       ||
    || account please enter "New" below.       ||
    || Please enter your login information:    ||
    =============================================
    Username: 
    """)

    #Get Username
    get_username = str(input())

    #If new then lets create a new account
    if (get_username == 'New'):
        create_account()
        print("Username: ")
        get_username = str(input())

    #Get Pin
    print("Pin: ")
    try:
        get_pin = int(input())
    except ValueError:
        print("Please enter a PIN with only integers.")
        logging.error("If you pressed enter then without any input then you probably got this error")
        

    #We authenticate the password and username by making sure there is only one instance of that pair in our database. If there are duplicates it would not work.
    mycursor.execute(f"SELECT count(*) AS counter FROM userlogins WHERE userName=('{get_username}') AND userPin=({get_pin})")
    myresult = mycursor.fetchall()
    for row in myresult:
        result = (row[0])
    count = result

    if (count == 1):
        print("Login authorized...")
        print("Loading the menu...")
        current_user = get_username
        current_pin = get_pin
        user = User(current_user)
        mycursor.execute(f"SELECT id FROM userlogins WHERE userName=('{current_user}') AND userPin=({current_pin})")
        myresult = mycursor.fetchall()
        for row in myresult:
            result = (row[0])
        current_id = result
        return (current_user, current_pin, current_id, user)
    else:
        print("You've entered the wrong credentials. Please try again or create a new account.")
        open_login()
            
def open_menu(current_user):
    """
    The main menu of the application.
    This will allow the user to interact with a GUI to decide what they want to do next with their bank account.
    Parameters:
        current_user: The username of the account we are currently logged into.
    Returns:
        result: The desired menu option that they want to interact with.
    """

    print(f""" 
       _______________________________________
     //   Welcome to Revature Banking, {current_user}   \\\\
    || ========================================||
    || 1. Check Balance                        ||
    || 2. Deposit Money                        ||
    || 3. Withdraw Money                       ||
    || 4. Transfer Money                       ||
    || 5. View Transaction History             ||
    || 6. Delete Account                       ||
    || 7. Exit                                 ||
    \\\\_________________________________________//
    """)
    print("Please enter a number (1-7) to continue: ")
    result = int(input())
    return result


def check_continue():
    """
    Function to check if the user want's to continue making transactions or interacting with the main menu.

    No parameters or returns.
    """
    print("Please enter \"Yes\" if you need to complete more transactions: ")
    result = str(input())
    if (result == 'Yes' or result == 'yes'):
        return True
    else:
        return False

def get_user_list():
    """
    Prints the list of all Usernames and their correponding User ID to pick the transfer receipient.

    No parameters or returns.
    """
    mycursor.execute("SELECT id, userName FROM userlogins")
    myresult = mycursor.fetchall()
    for row in myresult:
        id = (row[0])
        name = (row[1])
        print(f"ID: {id} Name: {name}")

def get_date():
    """
    Probably unneccessary but geting the date.

    Returns:
        now: The string of date and time at the current moment.
    """
    now = datetime.now()
    return now

def withdraw_from_sender(sender_id, transaction_amount):
    """
    Withdraw's money from the sender's account

    Paramenters:
        sender_id: The ID of the account logged in (who is sending money)
        transaction_amount: How much money we are sending/need to withdraw from the account.
    Returns: None
    """
    mycursor.execute(f"SELECT balance FROM userdata WHERE userdata.user_id='{sender_id}'")
    myresult = mycursor.fetchall()
    for row in myresult:
        result = (row[0])
    current_balance = result
    current_balance -= transaction_amount
    mycursor.execute(f"UPDATE userdata SET balance = {current_balance} WHERE user_id={sender_id}")
    mydb.commit()
    print("Your new balance is: " + str(current_balance))

def add_to_receiver(receiver_id, transaction_amount):
    """
    Deposit money in the user's account.

    Paramenters:
        receiver_id: The ID of the account user picked to send money to.
        transaction_amount: How much money we are sending/need to withdraw from the account.
    Returns: None
    """
    mycursor.execute(f"SELECT balance FROM userdata WHERE userdata.user_id={receiver_id}")
    myresult = mycursor.fetchall()
    for row in myresult:
        result = (row[0])
    current_balance = result
    current_balance += transaction_amount
    mycursor.execute(f"UPDATE userdata SET balance = {current_balance} WHERE user_id={receiver_id}")
    mydb.commit()
    mycursor.execute(f"SELECT userName FROM userlogins WHERE userlogins.id='{receiver_id}'")
    myresult = mycursor.fetchall()
    for row in myresult:
        result = (row[0])
    user_name = result
    print(f"${transaction_amount} has been added to {user_name}'s account.")

def add_transaction(sender_id, receiver_id, transaction_amount):
    """
    Add's transaction to database to allow us to keep a history of a certain account's transactions.

    Parameters:
        sender_id: The ID of the account logged in
        receiver_id: The ID of the account picked to send money to.
        transaction_amount: The amount of money being sent.
    Returns: None
    """
    sql = "INSERT INTO transactions (sender_id, receiver_id, transaction_date, transaction_amount) VALUES (%s, %s, %s, %s)"
    val = (sender_id, receiver_id, get_date(), transaction_amount)
    mycursor.execute(sql, val)
    mydb.commit()

def execute_transaction(sender_id, receiver_id, transaction_amount):
    """
    Executes all three neccessary functions to complete a transaction.

    Parameters:
        sender_id: The ID of the account logged in
        receiver_id: The ID of the account picked to send money to.
        transaction_amount: The amount of money being sent.
    Returns: None
    """
    withdraw_from_sender(sender_id, transaction_amount)
    add_to_receiver(receiver_id, transaction_amount)
    add_transaction(sender_id, receiver_id, transaction_amount)


def get_transaction_history(current_id):
    """
    Prints the account's transaction  history.

    Parameters:
        current_id: The ID of the account logged in.
    Returns: None
    """
    mycursor.execute(f"SELECT transaction_id, sender_id, receiver_id, transaction_date, transaction_amount FROM transactions WHERE sender_id={current_id} OR receiver_id={current_id}")
    myresult = mycursor.fetchall()
    for row in myresult:
        trans_id = row[0]
        sender_id = row[1]
        mycursor.execute(f"SELECT userName from userlogins WHERE id={sender_id}")
        saved_name = mycursor.fetchall()
        saved_sender = saved_name[0]
        receiver_id = row[2]
        mycursor.execute(f"SELECT userName from userlogins WHERE id={receiver_id}")
        saved_name = mycursor.fetchall()
        saved_receiver = saved_name[0]
        trans_date = row[3]
        trans_amount = row[4]
        print("Transaction ID: " + str(trans_id) + " | Sender ID: " + str(saved_sender) + " | Receiver ID: " + str(saved_receiver) + " | Transaction Date: " + str(trans_date) + " | Transaction Amount: $" + str(trans_amount))


def delete(user_id):
    """
    Delete's a user from both userdata and userlogins

    Paramenters:
        user_id: The user id of the account signed in, used to locate in database
    Returns:
        Boolean: True --> User was deleted return to login()
                 False --> User was not deleted return to menu()
    """
    print("Are you sure you want to delete? (Enter 'Yes' to confirm): ")
    confirm = str(input())
    if (confirm == 'Yes'):
        mycursor.execute(f"DELETE FROM userdata WHERE user_id='{user_id}'")
        mydb.commit()
        mycursor.execute(f"DELETE FROM transactions WHERE sender_id='{user_id}' OR receiver_id='{user_id}'")
        mydb.commit()
        mycursor.execute(f"DELETE FROM userlogins WHERE id='{user_id}'")
        mydb.commit()
        print("User Deleted. Taking you back to login.")
        return True
    else:
        print("Cancelled. Taking you back to the menu.")
        return False




def check_action(filter, user, current_user, current_pin, current_id):
    """
    Checks what action our user wants to take and executes the correct method.

    Parameters:
        Filter: the returned integer from open_menu() to decide what option to execute
        User: The User object
        current_user: The current username of the account logged in.
        current_pin: The current pin of the account logged in.
        current_id: The current id of the account logged in.
    """

    match filter:
        case 1: #Get balance
            user.get_balance(current_user, current_pin) 
            return True
        case 2: #Deposit Money
            user.deposit(current_user, current_pin) 
            return True
        case 3: #Withdraw Money
            user.withdraw(current_user, current_pin) 
        case 4: #Transfer money to another account
            print("""  _________________________________________
            //       Please Pick Transfer Recipient    \\
            =============================================
            """)
            get_user_list()
            print("Please enter the ID of the user: ")
            receiver_id = int(input())
            print("Please enter the amount you want to transfer: ")
            transaction_amount = float(input())
            execute_transaction(current_id, receiver_id, transaction_amount)
            return True
        case 5: #Get Transaction History
            get_transaction_history(current_id)
        case 6: #Delete User
            confirm = delete(current_id)
            if (confirm == True):
                open_login()
            else:
                open_menu(current_user)
        case 7: #Exit the application
            exit()

def main():
    """
    Main Driver of ATM
    """
    action = 1
    start = True
    (current_user, current_pin, current_id, this_user) = open_login()
    action = open_menu(current_user)
    while (start):
        start = check_action(action, this_user, current_user, current_pin, current_id)
        if (start == False):
            exit()
        start = check_continue()
        if (start == True):
            action = open_menu(current_user)
    exit()

#Run Main with all of our logic
main()
    
    
