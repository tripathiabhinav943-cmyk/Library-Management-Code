import mysql.connector
from datetime import date

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Abhinav",
        database="library_db"
    )

# Admin Functions
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add User")
        print("2. Search Users")
        print("3. Add Book")
        print("4. Modify Book")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Change Admin Credentials")
        print("8. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            search_users()
        elif choice == "3":
            add_book()
        elif choice == "4":
            modify_book()
        elif choice == "5":
            issue_book()
        elif choice == "6":
            return_book()
        elif choice == "7":
            change_admin_credentials()
        elif choice == "8":
            break
        else:
            print("Invalid choice.")

def add_user():
    username = input("Enter new username: ")
    password = input("Enter password: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    print("User added successfully.")

def search_users():
    keyword = input("Enter username keyword: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE username LIKE %s", ('%' + keyword + '%',))
    results = cur.fetchall()
    if results:
        for user in results:
            print(f"ID: {user[0]} | Username: {user[1]}")
    else:
        print("No users found.")

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    isbn = input("Enter ISBN: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)", (title, author, isbn))
    conn.commit()
    print("Book added successfully.")

def modify_book():
    book_id = input("Enter book ID to modify: ")
    title = input("New title: ")
    author = input("New author: ")
    isbn = input("New ISBN: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE books SET title=%s, author=%s, isbn=%s WHERE id=%s", (title, author, isbn, book_id))
    conn.commit()
    print("Book updated successfully.")

def issue_book():
    book_id = input("Enter book ID: ")
    user_id = input("Enter user ID: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE books SET issued_to=%s, issue_date=%s, return_date=NULL WHERE id=%s",
                (user_id, date.today(), book_id))
    conn.commit()
    print("Book issued successfully.")

def return_book():
    book_id = input("Enter book ID: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE books SET return_date=%s, issued_to=NULL WHERE id=%s", (date.today(), book_id))
    conn.commit()
    print("Book returned successfully.")

def change_admin_credentials():
    current_user = input("Current username: ")
    current_pass = input("Current password: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (current_user, current_pass))
    if cur.fetchone():
        new_user = input("New username: ")
        new_pass = input("New password: ")
        cur.execute("UPDATE admin SET username=%s, password=%s WHERE username=%s",
                    (new_user, new_pass, current_user))
        conn.commit()
        print("Admin credentials updated.")
    else:
        print("Invalid current credentials.")

# User Functions
def user_menu(user_id):
    while True:
        print("\n--- User Menu ---")
        print("1. View Available Books")
        print("2. View Issued Books")
        print("3. Add Note")
        print("4. View Notes")
        print("5. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            view_books()
        elif choice == "2":
            view_issued(user_id)
        elif choice == "3":
            add_note(user_id)
        elif choice == "4":
            view_notes(user_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def view_books():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author FROM books WHERE issued_to IS NULL")
    books = cur.fetchall()
    if books:
        for book in books:
            print(f"ID: {book[0]} | {book[1]} by {book[2]}")
    else:
        print("No books available.")

def view_issued(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT title, author, issue_date FROM books WHERE issued_to=%s", (user_id,))
    books = cur.fetchall()
    if books:
        for book in books:
            print(f"{book[0]} by {book[1]} issued on {book[2]}")
    else:
        print("No books issued.")

def add_note(user_id):
    title = input("Note title: ")
    content = input("Note content: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
    conn.commit()
    print("Note added.")

def view_notes(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT title, content FROM notes WHERE user_id=%s", (user_id,))
    notes = cur.fetchall()
    if notes:
        for note in notes:
            print(f"{note[0]}: {note[1]}")
    else:
        print("No notes found.")

# Main Menu
def main_menu():
    while True:
        print("\n=== Library Management System ===")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            username = input("Admin username: ")
            password = input("Password: ")
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            if cur.fetchone():
                admin_menu()
            else:
                print("Invalid admin credentials.")
        elif choice == "2":
            username = input("User username: ")
            password = input("Password: ")
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
            result = cur.fetchone()
            if result:
                user_menu(result[0])
            else:
                print("Invalid user credentials.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

main_menu()