#author_systems_sql is a module to manage all classes and functions related to authors in the advanced library managment system.
from connect_mysql import connect_database                                                                                                                               
from mysql.connector import DataError, Error

lib_conn = connect_database()


class Author:                                                                                                                                                   #establishing a class called author
    def __init__(self, name, birthday, hometown, author_id = None):                                                                                             #initializng the class
        self.__name = name                                                                                                                                      #private attribute
        self.__birthday = birthday                                                                                                                              #private attribute
        self.__hometown = hometown                                                                                                                              #private attribute
        self.__author_id = author_id
   
    @classmethod                                                                                                                                                #defining classmethod
    def create_table(cls):                                                                                                                                      #classmethod to create a data table
        if lib_conn is not None:                                                                                                                                #checking connection to database
            cursor = lib_conn.cursor()                                                                                                                          #establishing the cursor
            try:                                                                                                                                                #try block to help with error handling
               
                #query to create a table called Authors containing 4 columns
                query = '''CREATE TABLE IF NOT EXISTS Authors(                                                                                                      
                author_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                birthday DATE NOT NULL,
                hometown VARCHAR(255))'''

                cursor.execute(query)                                                                                                                           #calling the cursor to execute the query
                lib_conn.commit()                                                                                                                               #commiting the query to the database
                print("Table Authors is ready")                                                                                                                 #print statement letting the user know the table is ready
            
            except Error as e:                                                                                                                                  #except block to catch a general error
               print(f"Error: {e}")                                                                                                                             #print statement letting the user know there was an error
            
            finally:                                                                                                                                            #finally block to close the cursor
                cursor.close()
        
        else: print("Connection to database couldn't be established")                                                                                           #else statement telling the user conenction to the database couldnt be established
               
    @classmethod                                                                                                                                                #establishing a classmethod
    def create_author(cls, name, birthday, hometown):                                                                                                           #classmethod to create a class object
        new_author = cls(name, birthday, hometown)                                                                                                              #establishing the new object
        new_author.save_author()                                                                                                                                #calling the save author method to save the new author to the datatable
        return new_author                                                                                                                                       #returning the class object
    
    @classmethod                                                                                                                                                #establishing a classmethod
    def create_from_db(cls, table_row):                                                                                                                         #class method to create a class object from a datatable
        new_author = cls(table_row[1], table_row[2], table_row[3])                                                                                              #establishing the new class object, indexing the table row to get the needed values
        new_author.__author_id = table_row[0]                                                                                                                   #establishing new author id as the first column (0) of the table row
        return new_author                                                                                                                                       #returning the class object

    @classmethod                                                                                                                                                #establishing a classmethod
    def get_table_rows(cls):                                                                                                                                    #classmethod to get table row data from a datatable
        if lib_conn is not None:                                                                                                                                #checking connection to database
            cursor = lib_conn.cursor()                                                                                                                          #establishing a cursor
            try:                                                                                                                                                #try block for error handling
               
                query = "SELECT * FROM Authors"                                                                                                                 #query to select all from the authors table
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
    
    def get_bday(self):                                                                                                                                         #getter for birthday
        return self.__birthday
    
    def get_hometown(self):                                                                                                                                     #getter for hometown
        return self.__hometown
    
    def get_author_id(self):                                                                                                                                    #getter for author id
        return self.__author_id
    
    def save_author(self):                                                                                                                                      #defining a method to save a new author to the authors table
        if lib_conn is not None:                                                                                                                                #checking on the conncetion to the database
            cursor = lib_conn.cursor()                                                                                                                          #establishing a cursor

            try:                                                                                                                                                #try block to help with error handling
            
                query = "INSERT INTO Authors (name, birthday, hometown) VALUES (%s, %s, %s)"                                                                    #query to insert the data into the authors table, using placeholders for the data values
            
                cursor.execute(query, (self.__name, self.__birthday, self.__hometown))                                                                          #executing the query, passing in the object values as the expected values for the table
                lib_conn.commit()                                                                                                                               #commiting the data to the table
                self.__author_id = cursor.lastrowid                                                                                                             #setting author id to be the primary key of the table
                print("New author successfully added")                                                                                                          #print statement letting the user know the new author has been added
            
            except Error as e:                                                                                                                                  #except block for a general error
                print(f"Error: {e}")                                                                                                                            #print statement letting the user know there was an error
            
            finally:                                                                                                                                            #finally block closing the cursor
                cursor.close()
    
    def display_details(self):                                                                                                                                  #method to display author details
        print(f"\n{self.get_name()}:\nBorn - {self.get_bday()}\nHometown - {self.get_hometown()}")                                                              #print statement to print off details in a formatted way
    
    def display_name(self):                                                                                                                                     #method to display author name (honestly wasnt sure if i even needed this method since i can use the get_name method to do the same thing, but i wasnt sure if i should use a getter externally from the class or not)
        return self.get_name()                                                                                                                                  #returning the author name

    def display_id(self):
        return self.get_author_id()
    

def add_author():                                                                                                                                               #defining a funciton to add an author to the class
    try:                                                                                                                                                        #try block to help with error handling
        name = input("Enter the name of the author you wish to add: ").title()                                                                                  #obtaining user input
        birthday = input("Enter the author's birthday (YYYY-MM-DD): ")                                                                                          #obtaining user input
        hometown = input("Enter the author's hometown: ")                                                                                                       #obtaining user input
        name2 = name
        name = Author.create_author(name2, birthday, hometown)                                                                                                  #calling the classmethod create_author to establish an object of class Atuhor using the user inputs
        authors.append(name)                                                                                                                                    #appending the new object to the authors list
    
    except DataError():                                                                                                                                         #except block for a DataError
        print('Invalid input: Please enter the birthday in the format YYYY-MM-DD')                                                                              #print statement letting the user know they need to enter the birthday data in a certain format

def list_author_id():
    for author in authors:
        print(f"{Author.get_name(author)}: ID-{Author.get_author_id(author)}")

def list_authors():                                                                                                                                             #defining function to list the all authors
    for i, author in enumerate(authors):                                                                                                                        #for loop to cycle through all the authors in the list and enumerate to get the index numbers so they can be numbered
        print(f"{i + 1}. {Author.display_name(author)}")                                                                                                        #print statemeent printing off a numbered list of author names


def display_author_details():                                                                                                                                   #defining a function to display a certain authors details
    list_authors()                                                                                                                                              #calling the list authors function
    try:                                                                                                                                                        #try block to help with error handling
        auth_num = int(input("\nEnter the number of the author you wish to see the details for: "))                                                             #obtaining user input
        Author.display_details(authors[auth_num - 1])                                                                                                           #using user input to call a method from class Author
    
    except ValueError():                                                                                                                                        #except block for ValueError
        print("Invalid input: Please enter a the number of the author who's details you wish to view.")                                                         #letting the user know what the error was and how to prevent it

Author.create_table()
authors = Author.get_table_rows()                                                                                                                               #setting up an empty dictionary to hold the authors

def author_operations():                                                                                                                                        #defining a function for author operations
    
    while True:                                                                                                                                                 #setting up an infinite while loop so the user can cycle through choices
        print("\n1. Add a new author\n2. View author details\n3. Display all authors\n4. Exit")                                                                 #print statement list the functions the user can choose from
        author_choice = input("\nEnter the function you'd like to perform (1-4): ")                                                                             #variable author_choice is a user input
        print("\n")

        if author_choice == "1":                                                                                                                                #if block determining if the user selected choice 1
            add_author()
        
        elif author_choice =="2":                                                                                                                               #elif block determining if the user selected choice 2
            display_author_details()

        elif author_choice == "3":                                                                                                                              #elif block determining if the user selected choice 3
            list_authors()

        elif author_choice == "4":                                                                                                                              #elif block determining if the user selected choice 4
            lib_conn.close()
            break
            
        else: print("Input not recognized please enter a number 1-4 for your choice.")                                                                          #else block and print statement letting the user know their input wasnt recognized


