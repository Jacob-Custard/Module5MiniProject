#user_systems_sql is a module to manage all classes and functions related to users in the advanced library managment system.
from connect_mysql import connect_database                                                                                                                               
from mysql.connector import Error

lib_conn = connect_database()

class User:                                                                                                                                                     #establishing class called User
    def __init__(self, name, library_id, user_id = None):                                                                                                       #initiating class
        self.__name = name                                                                                                                                      #private attribute
        self.__library_id = library_id                                                                                                                          #private attribute
        self.__user_id = user_id                                                                                                                                #private attribute
       
    @classmethod                                                                                                                                                #establishing a classmethod
    def create_table(cls):                                                                                                                                      #classmethod to create a table
        if lib_conn is not None:                                                                                                                                #checking the connection to the database                                              
            cursor = lib_conn.cursor()                                                                                                                          #creating a cursor
            try:                                                                                                                                                #try block

                #query to create a table Users if one doesnt exist
                query = '''CREATE TABLE IF NOT EXISTS Users(
                user_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                library_id VARCHAR(10) UNIQUE NOT NULL)'''
            
                cursor.execute(query)                                                                                                                           #calling the cursor to execute the query
                lib_conn.commit()                                                                                                                               #commiting the table to the database
                print("Users table is ready")                                                                                                                   #print statement letting the user know the Users table is ready
                
            except Error as e:                                                                                                                                  #except block for a general error
                    print(f"Error: {e}")                                                                                                                        #print statement telling the user there was an error and what it is

            finally:                                                                                                                                            #finally block to close the cursor
                    cursor.close()

    @classmethod                                                                                                                                                #establishing a classmethod
    def create_user(cls, name, library_id):                                                                                                                     #classmethod to create a class object
        new_user = cls(name, library_id)                                                                                                                        #establishing the new object
        new_user.save_user()                                                                                                                                    #calling the save user method to save the new user to the datatable
        return new_user                                                                                                                                         #returning the class object
    
    @classmethod                                                                                                                                                #establishing a classmethod
    def create_from_db(cls, table_row):                                                                                                                         #class method to create a class object from a datatable
        new_user = cls(table_row[1], table_row[2])                                                                                                              #establishing the new class object, indexing the table row to get the needed values
        new_user.__user_id = table_row[0]                                                                                                                       #establishing new user id as the first column (0) of the table row
        return new_user                                                                                                                                         #returning the class object

    @classmethod                                                                                                                                                #establishing a classmethod
    def get_table_rows(cls):                                                                                                                                    #classmethod to get table row data from a datatable
        if lib_conn is not None:                                                                                                                                #checking connection to database
            cursor = lib_conn.cursor()                                                                                                                          #establishing a cursor
            
            try:                                                                                                                                                #try block for error handling               
                query = "SELECT * FROM Users"                                                                                                                   #query to select all from the users table
                cursor.execute(query)                                                                                                                           #calling the cursor to execute the query
                table_rows = cursor.fetchall()                                                                                                                  #fetching data with fetchall
                return [cls.create_from_db(row) for row in table_rows]                                                                                          #calling the create_from_db classmethod and returning the new class objects as a list
            
            except Error as e:                                                                                                                                  #except block for a general error
                print(f"Error: {e}")                                                                                                                            #print statement letting the user know there was an error
            
            finally:                                                                                                                                            #finally block closing the cursor
                cursor.close()
        
        else: print("Connection to database couldn't be established")                                                                                           #else statement letting the user know the program couldnt conenct to the database

    def get_name(self):                                                                                                                                         #getter for name
        return self.__name

    def get_lib_id(self):                                                                                                                                       #getter for library id
        return self.__library_id  
    
    def get_user_id(self):
        return self.__user_id

    def save_user(self):                                                                                                                                        #method to save a new user
        if lib_conn is not None:                                                                                                                                #checking on the conncetion to the database
            cursor = lib_conn.cursor()                                                                                                                          #establishing a cursor

            try:                                                                                                                                                #try block to help with error handling
            
                query = "INSERT INTO Users (name, library_id) VALUES (%s, %s)"                                                                                  #query to insert the data into the users table, using placeholders for the data values
            
                cursor.execute(query, (self.__name, self.__library_id))                                                                                         #executing the query, passing in the object values as the expected values for the table
                lib_conn.commit()                                                                                                                               #commiting the data to the table
                self.__user_id = cursor.lastrowid                                                                                                               #setting user id to be the primary key of the table
                print("New user successfully added")                                                                                                            #print statement letting the user know the new user has been added
            
            except Error as e:                                                                                                                                  #except block for a general error
                print(f"Error: {e}")                                                                                                                            #print statement letting the user know there was an error
            
            finally:                                                                                                                                            #finally block closing the cursor
                cursor.close()
    

    def user_details(self):                                                                                                                                     #method to display user details
        print(f"\n{self.get_name()}: Library ID - {self.get_lib_id()}\nBooks currently checkout to this user:")                                                 #print statement to format user details and present them to the user
        for book in self.loaned_books:                                                                                                                          #for loop to print all the books in loaned_books list
            print (book)
    
    def display_name(self):                                                                                                                                     #method to display user name (honestly wasnt sure if i even needed this method since i can use the get_name method to do the same thing, but i wasnt sure if i should use a getter externally from the class or not)
        return self.get_name()                                                                                                                                  #returning the user name


User.create_table()
user_ids = User.get_table_rows()                                                                                                                                #empty dictionary

def add_user():
    try:                                                                                                                                                        #try block for error handling
        user_name = input("Enter name of user: ")                                                                                                               #obtaining user input
        library_id = input("Enter new Library Id for user: ")                                                                                                   #obtaining user input
        library_id2 = library_id                                                                                                                                #setting new variable equal to original user input
        library_id = User.create_user(user_name, library_id2)                                                                                                   #setting up an object of Users
        user_ids.append(library_id)                                                                                                                             #appending class object to user_ids list
    
    except Error as e:                                                                                                                                          #except block for ValueError
        print(f"Error: {e}")
    

def list_all_users():                                                                                                                                           #function to list all user in user_ids dictionary
    for i, user in enumerate(user_ids):
        print(F"{i + 1}. {User.display_name(user)}")

def display_user_details():
    from Borrowed_books_sys import list_user_books
    list_all_users()
    user_input = int(input("Enter the number of the user you wish to see details for: "))
    User.user_details(user_ids[user_input - 1])
    user_id = User.get_user_id(user_ids[user_input - 1])
    list_user_books(user_id)

def user_operations():                                                                                                                                          #defining funciton for user operations
    while True:                                                                                                                                                 #establishing infinite while loop
        print("\n1. Add a new user\n2. View user details\n3. Display all users\n4. Exit")                                                                       #print statement listing the available options
        user_op_choice = input("Enter function you'd like to perform (1-4): ")                                                                                  #obtaining user input
        print("\n")
        
        if user_op_choice == "1":                                                                                                                               #if block determining if the user selected choice 1
            add_user()
        
        elif user_op_choice =="2":                                                                                                                              #elif block determining if the user selected choice 2
           display_user_details()
        
        elif user_op_choice == "3":                                                                                                                             #elif block determining if the user selected choice 3
            list_all_users()

        elif user_op_choice == "4":                                                                                                                             #elif block determining if the user selected choice 4
            lib_conn.close()
            break

        else: print("Input not recognized please enter a number 1-4 for your choice.")                                                                          #else block and print statement letting the user know their input wasnt recognized



