import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
            name VARCHAR(50) NOT null,
            surname VARCHAR(50) NOT null,
            email varchar(50)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
            client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE,
            phone VARCHAR(20)
        );
        """)

        conn.commit;


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name,surname,email) VALUES (%s, %s, %s);
        """, (first_name, last_name, email))
        conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone(client_id, phone) VALUES (%s, %s);
        """, (client_id, phone))
    conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if (first_name):
            cur.execute("""
            UPDATE client
            SET name = %s
            WHERE id = %s 
            """, (first_name, client_id))
        if (last_name):
            cur.execute("""
            UPDATE client
            SET surname = %s
            WHERE id = %s 
            """, (last_name, client_id))
        if (email):
            cur.execute("""
            UPDATE client
            SET email = %s
            WHERE id = %s 
            """, (email, client_id))
        conn.commit()


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone
        WHERE client_id = %s
        AND phone = %s
        ;
        """, (client_id, phone))
    conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client
        WHERE id = %s;
        """, (client_id,))
        conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    query: str = "SELECT c.*, p.phone FROM client c LEFT JOIN phone p ON p.client_id = c.id "
    if (first_name):
        query = query + "WHERE name = '" + first_name + "'"
    elif (last_name):
        query = query + "WHERE surname = '" + last_name + "'"
    elif (email):
        query = query + "WHERE email = '" + email + "'"
    query = query + "ORDER BY 1;"
    with conn.cursor() as cur:
        cur.execute(query)
        for id, name, surname, email, phone in cur.fetchall():
            print(f'ID: {id}, Имя: {name}, Фамилия: {surname}, Email: {email}, Телефон: {phone}')


if __name__ == "__main__":
    with psycopg2.connect(database="hw_clients", user="postgres", password="postgres") as conn:
        create_db(conn)
        add_client(conn, "name", "lastname", "test@test.com")
        add_client(conn, "name2", "lastname2", "test2@test.com")
        add_client(conn, "name3", "lastname3", "test3@test.com")
        add_client(conn, "name24", "lastname4", "test4@test.com")
        add_phone(conn, 1, "79500000000")
        add_phone(conn, 2, "79100011000")
        print("До изменений: ")
        find_client(conn)
        delete_client(conn, 3)
        delete_phone(conn, 2, "79100011000")
        change_client(conn, 1, last_name="Done")
        print("После изменений: ")
        find_client(conn)
        conn.close()
