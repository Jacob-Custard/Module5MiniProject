from connect_mysql import connect_database  
from mysql.connector import Error
import book_systems_sql as booksys
import author_systems_sql as authorsys
import user_systems_sql as usersys

lib_conn = connect_database()





def main():
     while True:
        print("\nWelcome to the Advanced Library Managment Application")
        print("\n1. Book Operations\n2. User Operations\n3. Author Operations\n4. Exit")
        user_choice = input("Enter function you'd like to perform (1-4): ")
        
        if user_choice == "1":                                                                                                                                  #if block determining if the user selected choice 1
            booksys.book_operations()
        
        elif user_choice =="2":                                                                                                                                 #elif block determining if the user selected choice 2
            usersys.user_operations()

        elif user_choice == "3":                                                                                                                                #elif block determining if the user selected choice 3
            authorsys.author_operations()

        elif user_choice == "4":                                                                                                                                #elif block determining if the user selected choice 4
            print("Thank you for using Advanced Library Managment Application!")
            lib_conn.close()
            break

        else: print("Input not recognized please enter a number 1-4 for your choice.")                                                                          #else block and print statement letting the user know their input wasnt recognized


main()