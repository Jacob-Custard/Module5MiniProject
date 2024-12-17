from connect_mysql import connect_database  
from mysql.connector import Error


lib_conn = connect_database()


class Borrowed_Book:                                                                                                                                            #establishing class called borrowed_book
    def __init__(self, title, user_id, book_id, borrow_date):                                                                                                   #initializing the class
        self.__title = title                                                                                                                                    #private attribute
        self.__user_id = user_id                                                                                                                                #private attribute
        self.__book_id = book_id                                                                                                                                #private attribute
        self.__borrow_date = borrow_date                                                                                                                        #private attribute
   
    @classmethod                                                                                                                                                #establishing classmethod
    def create_table(cls):                                                                                                                                      #classmethod to create a table
        if lib_conn is not None:                                                                                                                                #checking connection to database
            cursor = lib_conn.cursor()                                                                                                                          #establishing cursor
            try:                                                                                                                                                #try block to help with error handling
                query = '''CREATE TABLE IF NOT EXISTS Borrowed_Books(
                title VARCHAR(255) NOT NULL,
                user_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                book_id INT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES Books(book_id),
                borrow_date DATE NOT NULL)'''
                cursor.execute(query)                                                                                                                           #calling the cursor to execute the query
                lib_conn.commit()                                                                                                                               #commiting the data to the table
                print("Borrowed Books table is ready")                                                                                                          #print statement saying the table is ready
            
            except Error as e:                                                                                                                                  #except block for general error
                print(f"Error: {e}")

            finally:                                                                                                                                            #fianlly block to close the cursor
                cursor.close()
    
    @classmethod                                                                                                                                                #establishing a classmethod
    def create_borrowed_book(cls, title, user_id, book_id, borrow_date):                                                                                        #classmethod to create a class object
        borrowed_book = cls(title, user_id, book_id, borrow_date)                                                                                               #establishing the new object
        borrowed_book.save_borrowed_book()                                                                                                                      #calling the save author method to save the new borrowed book to the datatable
        return borrowed_book                                                                                                                                    #returning the class object
    
    @classmethod                                                                                                                                                #establishing a classmethod
    def create_from_db(cls, table_row):                                                                                                                         #class method to create a class object from a datatable
        borrowed_book = cls(table_row [0], table_row[1], table_row[2], table_row[3])                                                                            #establishing the new class object, indexing the table row to get the needed values
        return borrowed_book                                                                                                                                    #returning the class object

    @classmethod                                                                                                                                                #establishing a classmethod
    def get_table_rows(cls):                                                                                                                                    #classmethod to get table row data from a datatable
        if lib_conn is not None:                                                                                                                                #checking connection to database
            cursor = lib_conn.cursor()                                                                                                                          #establishing a cursor
            try:                                                                                                                                                #try block for error handling
               
                query = "SELECT * FROM Borrowed_Books"                                                                                                          #query to select all from the borrowed books table
                cursor.execute(query)                                                                                                                           #calling the cursor to execute the query
                table_rows = cursor.fetchall()                                                                                                                  #fetching data with fetchall
                return [cls.create_from_db(row) for row in table_rows]                                                                                          #calling the create_from_db classmethod and returning the new class objects as a list
            
            except Error as e:                                                                                                                                  #except block for a general error
                print(f"Error: {e}")                                                                                                                            #print statement letting the user know there was an error
            
            finally:                                                                                                                                            #finally block closing the cursor
                cursor.close()
        
        else: print("Connection to database couldn't be established")                                                                                           #else statement letting the user know the program couldnt conenct to the database
    
    def get_title(self):                                                                                                                                        #getter for title
        return self.__title
    
    def get_user_id(self):                                                                                                                                      #getter for user id
        return self.__user_id
    
    def get_book_id(self):                                                                                                                                      #getter for book id
        return self.__book_id
    
    def get_borrow_date(self):                                                                                                                                  #getter for borrow date
        return self.__borrow_date
    
    def get_author_id(self):                                                                                                                                    #getter for author id
        return self.__author_id
    
    def save_borrowed_book(self):                                                                                                                               #defining a method to save a new author to the authors table
        if lib_conn is not None:                                                                                                                                #checking on the conncetion to the database
            cursor = lib_conn.cursor()                                                                                                                          #establishing a cursor

            try:                                                                                                                                                #try block to help with error handling
            
                query = "INSERT INTO Borrowed_Books (title, user_id, book_id, borrow_date) VALUES (%s, %s, %s, %s)"                                             #query to insert the data into the borrowed books table, using placeholders for the data values
            
                cursor.execute(query, (self.__title, self.__user_id, self.__book_id, self.__borrow_date))                                                       #executing the query, passing in the object values as the expected values for the table
                lib_conn.commit()                                                                                                                               #commiting the data to the table
                            
            except Error as e:                                                                                                                                  #except block for a general error
                print(f"Error: {e}")                                                                                                                            #print statement letting the user know there was an error
            
            finally:                                                                                                                                            #finally block closing the cursor
                cursor.close()

def check_out_book(book_id):                                                                                                                                    #function to update the borrowed books table
    if lib_conn is not None:
        cursor = lib_conn.cursor()
        
        try:
            query = "UPDATE Books SET availability = 0 WHERE book_id = %s"
            cursor.execute(query, (book_id, ))
            lib_conn.commit()
        
        except Error as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()

def check_in_book(book_id):                                                                                                                                     #function to update the borrowed books table
    if lib_conn is not None:
        cursor = lib_conn.cursor()
        
        try:
            query = "UPDATE Books SET availability = 1 WHERE book_id = %s"
            cursor.execute(query, (book_id, ))
            lib_conn.commit()

        except Error as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()

def delete_book_row(user_id, book_id):                                                                                                                          #function to delete a row from borrowed_books
    if lib_conn is not None:
        cursor = lib_conn.cursor()
        try:
            query = "DELETE FROM Borrowed_Books WHERE user_id = %s AND book_id = %s"
            cursor.execute(query, (user_id, book_id))
            lib_conn.commit()

        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()    
def borrow_book():                                                                                                                                              #function to checkout a book to a user
    import book_systems_sql as booksys                                                                                                                          #importing the book systems moduel for this function
    try:                                                                                                                                                        #try block for error handling
        booksys.list_book_available()                                                                                                                           #calling a funciton from the books module
        book_number = int(input("Enter the number of the book you wish to check-out: "))                                                                        #user input 
        title = booksys.Book.display_title(booksys.books[book_number - 1])                                                                                      #using the class books to get the title of the book based off user input
        user_id = int(input("Enter your user_id: "))                                                                                                            #user input
        book_id = booksys.Book.get_book_id(booksys.books[book_number - 1])                                                                                      #establishing the book_id based off the first user input
        borrow_date = input("Enter the date the book is being checked out (YYYY-MM-DD): ")                                                                      #user input for the date
        title = str(title)
        title2 = title
        title = Borrowed_Book.create_borrowed_book(title2, user_id, book_id, borrow_date)                                                                       #establishing the class object
        borrowed_books.append(title)                                                                                                                            #appending the object to a list
        booksys.Book.loan_book(booksys.books[book_number - 1])                                                                                                  #calling the loan_book method from the Book class 

        check_out_book(book_id)                                                                                                                                 #calling the check_out_book function and passing in the established book_id variable
         
        print(f"{title2} has been checked out to user {user_id}")                                                                                               #print statement letting the user know the book has been checked out

    except ValueError:                                                                                                                                          #except block for value error
        print("user_id and book_id must be integers")
    
    except Error as e:                                                                                                                                          #except block for general error
        print(f"Error: {e}")
        
def return_book():                                                                                                                                              #establishing function to return a book
    import book_systems_sql as booksys                                                                                                                          #importing book systems module
    user_id = input("Enter your user_id: ")                                                                                                                     #user input to get user_id
    print("Here is the current list of books you have checked out")                                                                                             #print statement
    list_user_books(user_id)                                                                                                                                    #calling the list user books functon to list all books the user currently has checked out
    print("\nHere is the full list of books, please select which book you're returning.")                                                                       #print statement
    booksys.list_book_available()                                                                                                                               #list of all books for the user
    book_number = int(input("Enter the number of the book you are returning: "))                                                                                #user input
    book_id = booksys.Book.get_book_id(booksys.books[book_number - 1])                                                                                          #obrtaining the book_id using the user input
    booksys.Book.return_book(booksys.books[book_number - 1])                                                                                                    #calling the return book method from the Book class
    
    check_in_book(book_id)                                                                                                                                      #calling the check in bookm function and passing in the variable book_id
    delete_book_row(user_id, book_id)                                                                                                                           #calling the delete book row function and passing in the varibales user_id and book_id

    print("Book successfully returned")                                                                                                                         #print statment letting the user know the book was returned
          
def list_user_books(user_id):                                                                                                                                   #defining a function to list the books currently checked out to the user
    if lib_conn is not None:                                                                                                                                    #checking database connection
        cursor = lib_conn.cursor()                                                                                                                              #establishing cursor
        try:                                                                                                                                                    #try block for error handling
            query = "SELECT title, book_id FROM Borrowed_Books WHERE user_id = %s"                                                                              #query to get the title and book_id from the datatable for the books that have the inputted user_id 
            cursor.execute(query, (user_id, ))                                                                                                                  #calling the cursor to execute the query
            books = cursor.fetchall()                                                                                                                           #fetchall to get the row
            for row in books:                                                                                                                                   #for loop to print off the rows called
                print(row)
        
        except Error as e:                                                                                                                                     #except block for general error
            print(f"Error: {e}")

Borrowed_Book.create_table()                                                                                                                                    #establishing the borrowed_books table if it doesnt alredy exist
borrowed_books = Borrowed_Book.get_table_rows()                                                                                                                 #establihsing a borrowed_books list
