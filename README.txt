Advanced Library Managment System SQL

Description:
    This system is intended to manage a library. The system consists of a library of books, users, and authors, and integrates wit a SQL database.
The program is made up of 5 modules, Borrowed_book_sys, book_systems_sql, user_systems_sql, author_systems_sql, and the main module Advanced Library 
Managment System SQL. The program also consists of 4 tables stored in a MySQL database. The tables are Authors, Books, Users, and Borrowed_Books. 
The author module is made up of the Author class and connects to the Authors table in the database. This module gives the user the ability to add authors
to the database, view author details, and list all the authors currently in the database. The Authors table stores an author id number as a primary key, 
name, birthday and hometown. The book module has the Book class and connects to the Books table. The module allows the user to add a book, check out a book, 
return a book, search for a book, and look at the details of a book. The Books table stores book id as a primary key, title, author id as a foreign key linked to the Authors tale, genre,
isbn, publicaiton date, and availability. Since author id is a foreign key an author must exist before a book can be created. The User module is made up of the 
User class and connects to the Users table. With this module the user can create a user, get user details, and list all users. The Users table keep the users name, 
library id, and user id as the primary key. The borrowed books module consists of the borrwoed book class and connects to the Borrowed Books table. This module helps 
to facilitate the check out and check in process in the book module. The Borrowed Books table is simply meant to keep track of which user has checked out which books.
As such it has no primary key of its own, and is instead made up of book title, user id, which is a foregin key linked to the Users table, book id as a foreign key
linked to the Books table, and borrow date.

Instructions:
1. Load the Advanced Library Managment System SQL file
2. Run the "main' function
3. Select operation set
4. Select function
5. Follow on screen prompts 
6. Cycle through operation sets and functions until finished
7. Exit the program
-- note: an author must exist in order to create a book
-- note: a book and a user must exist before a book can be checked out

sources:
1. https://stackoverflow.com/questions/1250103/attributeerror-module-object-has-no-attribute
2. https://medium.com/@joeylee08/object-relational-mapping-from-python-to-sql-and-back-cd629eca0060

github repository: https://github.com/Jacob-Custard/Module5MiniProject