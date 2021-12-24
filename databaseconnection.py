from getpass import getpass
from mysql.connector import connect, Error
import hashlib

# takes in a string object and converts it into a hash
def sha256Encription(message):
    encrypted = hashlib.sha256(message.encode()).hexdigest()
    return encrypted

#Creates new user account in the database
def createAccount():
    
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="second_database",

        ) as connection:
            with connection.cursor() as cursor:
                create_user_query = """INSERT INTO users
    (name, password)
    VALUES ( %s, %s )
    """
                print("Create New User:")
                username = input("Enter Username: ")
                password = getpass("Enter User Password: ")
                hashedPassword = sha256Encription(password)
                user_record = [
                    (username, hashedPassword),
                    ]
                cursor.executemany(create_user_query, user_record)
                connection.commit()
                print("You have successfully created an account!")
                
    except Error as e:
        print(e)

#Checks user credentials for a secure login 
def login():
      
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="second_database",

        ) as connection:
            with connection.cursor() as cursor:
                print("Log on to an existing account:")
                username = input("Enter Username: ")
                password = getpass("Enter User Password: ")
                hashedPassword = (sha256Encription(password))
                user_query = """SELECT password FROM users WHERE name = \"{}\"  """.format(username)
                cursor.execute(user_query)
                for row in cursor:
                    databasedPassword = row[0]
                    if hashedPassword == databasedPassword:
                        print("You Have Successfully logged in!")
                    else:
                        print("Login Failed. \nPlease check username/password and try again")
            #Do something here once the user has successfully logged in 
                    
    except Error as e:
        print(e)
    


def main():
    task = input("To create an account type 'a' then press enter \n       To login press just press enter: ")
    print("Log into the server: \n\n")
    if task == "a":
        createAccount()
    else:
        login()
    
    
if __name__ == '__main__':
     main()
