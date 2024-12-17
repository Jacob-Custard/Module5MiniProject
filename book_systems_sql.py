#book_systems_sql is a module to manage all classes and functions related to books in the advanced library managment system.
from connect_mysql import connect_database                                                                                                                               
from mysql.connector import Error
import user_systems_sql as usersys
from author_systems_sql import list_author_id

lib_conn = connect_database()


class Book:                                                                                                                                                                   #establishing a class called Book
    def __init__(self, title, author_id, genre, isbn, publication_date, book_id = None):                                                                                      #initializing the class
        self.__book_id = book_id
        self.__title = title                                                                                                                                                  #private attribute
        self.__author_id = author_id                                                                                                                                          #private attribute
        self.__genre = genre                                                                                                                                                  #private attribute
        self.__isbn = isbn
        self.__publication_date = publication_date                                                                                                                            #private attribute
        self.__available = 1                                                                                                                                                  #private attribute
    
    @classmethod                                                                                                                                                              #establishing a classmethod
    def create_table(cls):                                                                                                                                                    #classmethod to create a table
        if lib_conn is not None:                                                                                                                                              #checking the connection to the database
            cursor = lib_conn.cursor()                                                                                                                                        #creating a cursor
            try:                                                                                                                                                              #try block for error handling

                query = '''CREATE TABLE IF NOT EXISTS Books(
                book_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                title VARCHAR(255) NOT NULL,
                author_id INT NOT NULL,
                FOREIGN KEY (author_id) REFERENCES Authors(author_id),
                genre VARCHAR(255),
                isbn VARCHAR(13) NOT NULL,
                publication_date DATE,
                availability BOOLEAN DEFAULT 1)'''

                cursor.execute(query)                                                                                                                                         #calling the cursor to execute the query
                lib_conn.commit()                                                                                                                                             #commiting the table to the database
                print("Books Table is ready")                                                                                                                                 #print statement letting the user know the Books table is ready

            except Error as e:                                                                                                                                                #except block for general error
                print(f"Error: {e}")

            finally:                                                                                                                                                          #finally block to close the cursor
                cursor.close()

    @classmethod                                                                                                                                                              #establishing classmethod
    def create_book(cls, title, author_id, genre, isbn, publication_date):                                                                                                    #classmethod to create a class object
        new_book = cls(title, author_id, genre, isbn, publication_date)                                                                                                       #establishing the new object
        new_book.save_book()                                                                                                                                                  #calling the save book method to save the new book to the datatable
        return new_book                                                                                                                                                       #returning the class object
    
    @classmethod                                                                                                                                                              #establishing a classmetho
    def create_from_db(cls, table_row):                                                                                                                                       #class method to create a class object from a datatable
        new_book = cls(table_row[1], table_row[2], table_row[3], table_row[4], table_row[5])                                                                                  #establishing the new class object, indexing the table row to get the needed values
        new_book.__book_id = table_row[0]                                                                                                                                     #establishing new user id as the first column (0) of the table row
        return new_book                                                                                                                                                       #returning the class object
    
    @classmethod                                                                                                                                                              #establishing a classmethod
    def get_table_rows(cls):                                                                                                                                                  #classmethod to get table row data from a datatable
        if lib_conn is not None:                                                                                                                                              #checking connection to database
            cursor = lib_conn.cursor()                                                                                                                                        #establishing a cursor

            try:                                                                                                                                                              #try block for error handling
                query = "SELECT * FROM Books"                                                                                                                                 #query to select all from the users table
                cursor.execute(query)                                                                                                                                         #calling the cursor to execute the query
                table_rows = cursor.fetchall()                                                                                                                                #fetching data with fetchall
                return [cls.create_from_db(row) for row in table_rows]                                                                                                        #calling the create_from_db classmethod and returning the new class objects as a list
            
            except Error as e:                                                                                                                                                #except block for a general error
                print(f"Error: {e}")

            finally:                                                                                                                                                          #finally block closing the cursor
                cursor.close()
        
        else:
            print("Connection to database couldnt be established")
    
    def save_book(self):                                                                                                                                                      #method to save a new book
        if lib_conn is not None:                                                                                                                                              #checking on the conncetion to the database
            cursor = lib_conn.cursor()                                                                                                                                        #establishing a cursor

            try:                                                                                                                                                              #try block to help with error handling
                
                query = "INSERT INTO Books (title, author_id, genre, isbn, publication_date) VALUES (%s, %s, %s, %s, %s)"                                                     #query to insert the data into the users table, using placeholders for the data values
                
                cursor.execute(query, (self.__title, self.__author_id, self.__genre, self.__isbn, self.__publication_date))                                                   #executing the query, passing in the object values as the expected values for the table
                lib_conn.commit()                                                                                                                                             #commiting the data to the table
                self.__book_id = cursor.lastrowid                                                                                                                             #setting book id to be the primary key of the tabl
                print("New book added successfully")                                                                                                                          #print statement letting the user know the new user has been added

            except Error as e:                                                                                                                                                #except block for a general error
                print(f"Error: {e}")

            finally:                                                                                                                                                          #finally block closing the cursor
                cursor.close()

    def get_title(self):                                                                                                                                                      #getter for title
        return self.__title  
    
    def get_author(self):                                                                                                                                                     #getter for author
        return self.__author_id
    
    def get_genre(self):                                                                                                                                                      #getter for genre
        return self.__genre 
    
    def get_pub_date(self):                                                                                                                                                   #getter for publication year
        return self.__publication_date
    
    def get_available(self):                                                                                                                                                  #getter for available
        return self.__available   

    def get_isbn(self):
        return self.__isbn

    def get_book_id(self):
        return self.__book_id

    def loan_book(self):                                                                                                                                                      #method to loan books
        self.__available = 0                                                                                                                                                  #changing available attribute to False
        
    
    def return_book(self):                                                                                                                                                    #method to return books                                                                                                                                  
        self.__available = 1                                                                                                                                                  #changing available attribute to True
    
    def display_details(self):                                                                                                                                                #method to display book details
        print(f"\nTitle: {self.get_title()}\nAuthor: {self.get_author()}\nGenre: {self.get_genre()}\nISBN: {self.get_isbn()}\nPublication Year: {self.get_pub_date()}\n")     #printing off book details using getters
        if self.get_available(): print("Availability: Available")
        else: print("Availability: Not Available")
    
    def display_title(self):
        return self.get_title()
    
 



def add_book():                                                                                                                                                               #defining a function to add a book to the class
    try:
        title = input("Enter the title of the book you want to add: ").strip().title()                                                                                        #obtaining user input, added .title() for formatting 
        list_author_id()
        author_id = int(input("Enter the ID number of the book's author from the provided list: "))                                                                           #obtaining user input, added .title() for formatting
        genre = input("Enter book's genre: ").strip().title()                                                                                                                 #obtaining user input, added .title() for formatting
        isbn = input("Enter the isbn of the book: ")
        publication_date = input("Enter the publication date (YYYY-MM-DD): ")                                                                                                 #obtaining user input
        title2 = title                                                                                                                                                        #second title variable set to the original user input
        title = Book.create_book(title2, author_id, genre, isbn, publication_date)
        books.append(title)
    
    except ValueError:
        print("\nPublication year must be a 4 digit whole number.")


def search_book():                                                                                                                                                            #defining a fcuntion to search for a specific book
    list_books()
    book = int(input("Enter the number of the book you're searching for: "))
    Book.display_details(books[book - 1])  

def list_book_available():
    for i, book in enumerate(books):
        if Book.get_available(book) == 1:
            print(f"{i + 1}. {Book.display_title(book)}: available")
        else:
            print(f"{i + 1}. {Book.display_title(book)}: not available")

def list_books():                                                                                                                                                             #defining a function to list all books
    for i, book in enumerate(books):                                                                                                                                          #for loop to cycle through the books dictionary
        print(f"{i + 1}. {Book.display_title(book)}")                                                                                                                         #printing each book

Book.create_table()
books = Book.get_table_rows()                                                                                                                                                 #empty list

def book_operations():                                                                                                                                                        #defining function called book operations
    import Borrowed_books_sys as borrowedbooks
    while True:                                                                                                                                                               #infinite while loop
        print("\n1. Add a new book\n2. Borrow a book\n3. Return a book\n4. Search for a book\n5. Display all books\n6. Exit")                                                 #print statement listing the users options
        book_choice = input("Enter the function you'd like to perform (1-6): ")                                                                                               #obtaining a user input
        print("\n")                                                                                                                                                           #new line for a little bit of formatting

        if book_choice == "1":                                                                                                                                                #if block determining if the user selected choice 1
            add_book()
        
        elif book_choice =="2":                                                                                                                                               #elif block determining if the user selected choice 2
           
           borrowedbooks.borrow_book()

        elif book_choice == "3":                                                                                                                                              #elif block determining if the user selected choice 3
           borrowedbooks.return_book()
       
        elif book_choice == "4":                                                                                                                                              #elif block determining if the user selected choice 4
            search_book()

        elif book_choice == "5":                                                                                                                                              #elif block determining if the user selected choice 5
            list_books()

        elif book_choice == "6":                                                                                                                                              #elif block determining if the user selected choice 6
            lib_conn.close()
            break

        else: print("Input not recognized please enter a number 1-4 for your choice.")                                                                                        #else block and print statement letting the user know their input wasnt recognized



        
     

