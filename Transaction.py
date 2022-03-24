import mysql.connector
from datetime import datetime

class Transaction:

    global mycursor
    global mydb
    global myresult

    # Set up our database connection so we can interact with a User's bank account with the SQL Database.
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sqlProject0",
    database = "demodatabase"
    )
    mycursor = mydb.cursor()

    def __init__(self, sender_id, receiver_id, transaction_amount):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.transaction_amount = transaction_amount
    
    def get_date():
        now = datetime.now
        return now.strftime("%m/%d/%Y, %H:%M:%S")

    # Get current balance to display
    # Subtract transaction amount from sender's current balance
    # Update SQL Database
    # Confirm Completion
    def withdraw_from_sender(self):
        mycursor.execute(f"SELECT balance FROM userdata WHERE userdata.user_id='{self.sender_id}'")
        myresult = mycursor.fetchall()
        for row in myresult:
            result = (row[0])
        current_balance = result
        current_balance -= self.transaction_amount
        mycursor.execute(f"UPDATE userdata SET balance = {current_balance} WHERE user_id={self.sender_id}")
        mydb.commit()
        print("Your new balance is: " + str(current_balance))

    def add_to_receiver(self):
        mycursor.execute(f"SELECT balance FROM userdata WHERE userdata.user_id='{self.receiver_id}'")
        myresult = mycursor.fetchall()
        for row in myresult:
            result = (row[0])
        current_balance = result
        current_balance += self.transaction_amount
        mycursor.execute(f"UPDATE userdata SET balance = {current_balance} WHERE user_id={self.receiver_id}")
        mydb.commit()
        mycursor.execute(f"SELECT userName FROM userlogins WHERE userlogins.id={self.receiver_id}")
        for row in myresult:
            result = (row[0])
        user_name = result
        print(f"${self.transaction_amount} has been added to {user_name}'s account.")

    def add_transaction(self):
        sql = "INSERT INTO transactions (sender_id, receiver_id, transaction_date, transaction_amount) VALUES (%i, %i, %s, %f)"
        val = (self.sender_id, self.receiver_id, self.get_date(), self.transaction_amount)
        mycursor.execute(sql, val)
        mydb.commit()

    def execute_transaction(self, sender_id, receiver_id):
        self.withdraw_from_sender()
        self.add_to_receiver()
        self.add_transaction()