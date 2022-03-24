# global mydb
# global mycursor
# global current_user
# global current_pin
# global current_id
# global user

# def open_login():
#     print("""  _____________________________________
#     //       Welcome to Revature Banking       \\
#     || If you need to register for a new       ||
#     || account please enter "New" below.       ||
#     || Please enter your login information:    ||
#     """)
#     get_username = str(input())

#     if (get_username == 'New'):
#         self.create_account()
#     else:
#         print("Pin: ")
#         try:
#             get_pin = int(input())
#         except ValueError:
#             print("Please enter a PIN with only integers.")
#         mycursor.execute(f"SELECT count(*) AS counter FROM userlogins WHERE userName=('{get_username}') AND userPin=({get_pin})")
#         myresult = mycursor.fetchall()
#         for row in myresult:
#             result = (row[0])
#         count = result

#         if (count == 1):
#             print("Login authorized...")
#             print("Loading the menu...")
#             current_user = get_username
#             current_pin = get_pin
#             user = User(current_user)
#             mycursor.execute(f"SELECT id FROM userlogins WHERE userName=('{current_user}') AND userPin=({current_pin})")
#             myresult = mycursor.fetchall()
#             for row in myresult:
#                 result = (row[0])
#             current_id = result
#             return (current_user, current_pin, current_id, user)
#         else:
#             print("You've entered the wrong credentials. Please try again or create a new account.")
#             self.open_login()

# open_login()

def sum():
    print(2+2)

sum()