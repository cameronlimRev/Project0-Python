from unicodedata import name
import mysql.connector
from datetime import datetime


class User:

    global mydb
    global mycursor
    global myresult

    # Set up our database connection so we can interact with a User's bank account with the SQL Database.
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sqlProject0",
    database = "demodatabase"
    )
    mycursor = mydb.cursor()

    # mycursor.execute("SELECT * from demodatabase.transactions")
    # myresult = mycursor.fetchall()

    # for x in myresult:
    #     print(x)

    def __init__(self, name):
        self.name = name
        self.balance = 5000

    def get_name(): 
        return name
    
    def get_balance(self, current_user, current_pin):
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT balance FROM userdata WHERE userdata.user_id=(SELECT id from userlogins WHERE userName='{current_user}' AND userPin='{current_pin}')")
        myresult = mycursor.fetchall()
        for row in myresult:
            result = (row[0])
        print(f"Your current balance is: ${result}.")
        return result

# User can deposit money from their bank account.
# We will print the current balance
# Get amount to deposit
# Apply calculations to bank account
# Update SQL Database
# Create a transaction record

    def deposit(self, current_user, current_pin):
        mycursor.execute(f"SELECT balance FROM userdata WHERE userdata.user_id=(SELECT id from userlogins WHERE userName='{current_user}' AND userPin='{current_pin}')")
        myresult = mycursor.fetchall()
        for row in myresult:
            result = (row[0])
        current_balance = result
        print(f"Your balance before the transaction: ${result}.")
        print("Please enter the amount you are depositing: $")
        transaction_amount = -1
        while (transaction_amount < 0):
            try:
                transaction_amount = float(input())
            except ValueError:
                print("Invalid input. Please try again.")
        current_balance += transaction_amount
        print(f"Your new balance is: ${round(current_balance,2)}.")
        mycursor.execute(f"UPDATE userdata SET balance = {round(current_balance,2)} WHERE user_id=(SELECT id from userlogins WHERE userName='{current_user}' AND userPin='{current_pin}')")
        mydb.commit()
        print("Your balance has been updated.")
        add_to_transactions(self, current_user, current_pin, transaction_amount)

# User can withdraw money from their bank account.
# We will print the current balance
# Get amount to withdraw
# Apply calculations to bank account
# Update SQL Database
# Create a transaction record.
    def withdraw(self, current_user, current_pin):
            mycursor.execute(f"SELECT balance FROM userdata WHERE userdata.user_id=(SELECT id from userlogins WHERE userName='{current_user}' AND userPin='{current_pin}')")
            myresult = mycursor.fetchall()
            for row in myresult:
                result = (row[0])
            current_balance = result
            print(f"Your balance before the transaction: ${result}.")
            print("Please enter the amount you are withdrawing: $")
            transaction_amount = -1
            while (transaction_amount < 0):
                try:
                    transaction_amount = float(input())
                except ValueError:
                    print("Invalid input. Please try again.")
            if (current_balance-transaction_amount > 0):
                current_balance -= transaction_amount
            print(f"Your new balance is: ${round(current_balance,2)}.")
            mycursor.execute(f"UPDATE userdata SET balance = {round(current_balance,2)} WHERE user_id=(SELECT id from userlogins WHERE userName='{current_user}' AND userPin='{current_pin}')")
            mydb.commit()
            print("Your balance has been updated.")
            transaction_amount = -transaction_amount
            add_to_transactions(self, current_user, current_pin, transaction_amount)

# This will add to the Transactions table to keep a transaction history of their bank account.
# This could be used with the transactions class add_transaction; however I chose to do it locally since sender and receiver id will not be unique.
def add_to_transactions(self, current_user, current_pin, transaction_amount):
    mycursor.execute(f"SELECT id FROM userlogins WHERE userName=('{current_user}') AND userPin=('{current_pin}')")
    myresult = mycursor.fetchall()
    for row in myresult:
        result = (row[0])
    current_id = result

    now = datetime.now() #Get our current date and time.
    sql = "INSERT INTO transactions (sender_id, receiver_id, transaction_date, transaction_amount) VALUES (%s, %s, %s, %s)"
    val = (current_id, current_id, now.strftime("%m/%d/%Y, %H:%M:%S"), transaction_amount)

    mycursor.execute(sql, val)
    mydb.commit()

    print("Added to transaction history.")
    