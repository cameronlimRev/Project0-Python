import mysql.connector

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



mycursor.execute(f"SELECT userName FROM userlogins WHERE userlogins.id='{receiver_id}'")
myresult = mycursor.fetchall()
for row in myresult:
    result = (row[0])
user_name = result


mycursor.execute("SELECT balance FROM userdata WHERE userdata.user_id=")
myresult = mycursor.fetchall()
for row in myresult:
    result = row[0]
print(f"Your current balance is: ${result}.")

# for x in myresult:
#     print(x[0])

pip3 install mysql-connector-python