from connect import connect


def search_pattern():
    pattern = input("Enter pattern: ")
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def upsert_one():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()

    print("Saved")

    cur.close()
    conn.close()


def insert_many():
    names = ["Ali", "Aruzhan", "Dias"]
    phones = ["87771234567", "abc123", "+77015554433"]

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()

    print("Bulk insert done")

    cur.close()
    conn.close()


def show_paginated():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_data():
    value = input("Enter username or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    print("Deleted")

    cur.close()
    conn.close()


while True:
    print("\n1. Search by pattern")
    print("2. Insert or update one contact")
    print("3. Insert many contacts")
    print("4. Show paginated contacts")
    print("5. Delete by username or phone")
    print("6. Exit")

    choice = input("Choose: ")

    if choice == "1":
        search_pattern()
    elif choice == "2":
        upsert_one()
    elif choice == "3":
        insert_many()
    elif choice == "4":
        show_paginated()
    elif choice == "5":
        delete_data()
    elif choice == "6":
        break
    else:
        print("Wrong choice")