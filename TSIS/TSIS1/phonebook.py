import csv
import json
from datetime import datetime
from connect import get_connection

VALID_PHONE_TYPES = {"home", "work", "mobile"}


def parse_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return
    for row in rows:
        print(row)


# ---------------- ADD CONTACT ----------------
def add_contact():
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip() or None
    birthday_input = input("Enter birthday (YYYY-MM-DD or empty): ").strip()
    group_name = input("Enter group: ").strip() or "Other"

    try:
        birthday = parse_date(birthday_input) if birthday_input else None
    except:
        print("Invalid date")
        return

    phones = []
    while True:
        phone = input("Enter phone (leave empty to stop): ").strip()
        if not phone:
            break
        ptype = input("Type [home/work/mobile]: ").strip().lower()
        if ptype not in VALID_PHONE_TYPES:
            print("Invalid type")
            continue
        phones.append((phone, ptype))

    if not phones:
        print("Need at least one phone")
        return

    conn = get_connection()
    cur = conn.cursor()

    # group
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING",
        (group_name,),
    )
    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    group_id = cur.fetchone()[0]

    # contact
    cur.execute(
        "INSERT INTO contacts(name,email,birthday,group_id) VALUES (%s,%s,%s,%s) RETURNING id",
        (name, email, birthday, group_id),
    )
    contact_id = cur.fetchone()[0]

    # phones
    for phone, ptype in phones:
        cur.execute(
            "INSERT INTO phones(contact_id,phone,type) VALUES (%s,%s,%s)",
            (contact_id, phone, ptype),
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added ✅")


# ---------------- SEARCH ----------------
def search_all():
    q = input("Enter search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT c.name,c.email,c.birthday,g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id=c.group_id
        WHERE c.name ILIKE %s OR c.email ILIKE %s
        """,
        (f"%{q}%", f"%{q}%"),
    )

    print_contacts(cur.fetchall())

    cur.close()
    conn.close()


def search_email():
    q = input("Enter email: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT name,email FROM contacts WHERE email ILIKE %s",
        (f"%{q}%",),
    )

    print_contacts(cur.fetchall())

    cur.close()
    conn.close()


# ---------------- FILTER ----------------
def filter_group():
    group = input("Enter group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT c.name,c.email,g.name
        FROM contacts c
        JOIN groups g ON g.id=c.group_id
        WHERE g.name=%s
        """,
        (group,),
    )

    print_contacts(cur.fetchall())

    cur.close()
    conn.close()


# ---------------- SORT ----------------
def sort_contacts():
    key = input("Sort by [name/birthday]: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT name,email,birthday FROM contacts ORDER BY {key}")

    print_contacts(cur.fetchall())

    cur.close()
    conn.close()


# ---------------- PAGINATION ----------------
def paginate():
    limit = int(input("Enter page size: "))
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    while True:
        cur.execute(
            "SELECT name,email FROM contacts LIMIT %s OFFSET %s",
            (limit, offset),
        )
        rows = cur.fetchall()

        print("\nPage:", offset)
        print_contacts(rows)

        cmd = input("next/prev/quit: ")
        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

    cur.close()
    conn.close()


# ---------------- JSON ----------------
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name,email FROM contacts")
    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f)

    print("Exported")

    cur.close()
    conn.close()


def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for name, email in data:
        cur.execute(
            "INSERT INTO contacts(name,email) VALUES (%s,%s)",
            (name, email),
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Imported")


# ---------------- EXTRA ----------------
def add_phone():
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()


def move_group():
    name = input("Name: ")
    group = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s,%s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()


# ---------------- MAIN ----------------
def main():
    while True:
        print("\n========== EXTENDED PHONEBOOK ==========")
        print("1 Add contact")
        print("2 Search all")
        print("3 Search email")
        print("4 Filter group")
        print("5 Sort")
        print("6 Pagination")
        print("7 Export JSON")
        print("8 Import JSON")
        print("10 Add phone")
        print("11 Move group")
        print("0 Exit")

        c = input("Choose: ")

        if c == "1":
            add_contact()
        elif c == "2":
            search_all()
        elif c == "3":
            search_email()
        elif c == "4":
            filter_group()
        elif c == "5":
            sort_contacts()
        elif c == "6":
            paginate()
        elif c == "7":
            export_json()
        elif c == "8":
            import_json()
        elif c == "10":
            add_phone()
        elif c == "11":
            move_group()
        elif c == "0":
            break


if __name__ == "__main__":
    main()