from connect import connect
import csv

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100),
        phone VARCHAR(20) UNIQUE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created!")

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact added!")
    except:
        print("Error")

    cur.close()
    conn.close()

def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                    (row["first_name"], row["phone"])
                )
            except:
                pass

    conn.commit()
    cur.close()
    conn.close()
    print("CSV added!")

def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def update_contact():
    name = input("Enter name: ")
    new_phone = input("New phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE first_name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Updated!")

def delete_contact():
    name = input("Enter name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted!")

def menu():
    while True:
        print("\n1.Create table")
        print("2.Insert console")
        print("3.Insert CSV")
        print("4.Show all")
        print("5.Update")
        print("6.Delete")
        print("7.Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            show_all()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            break

if __name__ == "__main__":
    menu()

