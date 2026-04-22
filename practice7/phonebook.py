import csv
from connect import connect


# 1. Создание таблицы
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created")


# 2. Добавление вручную
def insert_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Added")


# 3. Загрузка из двух CSV файлов
def insert_from_multiple_csv(files):
    conn = connect()
    cur = conn.cursor()

    for filename in files:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # пропустить заголовок

            for row in reader:
                if len(row) < 2:
                    continue

                name = row[0].strip()
                phone = row[1].strip()

                cur.execute(
                    "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                    (name, phone)
                )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted")


# 4. Показать все
def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# 5. Обновление
def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Updated")


# 6. Удаление
def delete_contact():
    name = input("Enter name to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name = %s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")


# МЕНЮ
while True:
    print("""
1. Create table
2. Insert console
3. Insert CSV (2 files)
4. Show all
5. Update
6. Delete
7. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        create_table()
    elif choice == "2":
        insert_console()
    elif choice == "3":
        insert_from_multiple_csv(["contacts.csv", "contacts1.csv"])
    elif choice == "4":
        show_all()
    elif choice == "5":
        update_contact()
    elif choice == "6":
        delete_contact()
    elif choice == "7":
        break
    else:
        print("Wrong choice")