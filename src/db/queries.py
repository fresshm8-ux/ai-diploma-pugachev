def get_all_candidates(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM candidates")
    return cursor.fetchall()

candidates = get_all_candidates(connection)

for candidate in candidates:
    print(candidate)

def find_candidates_by_city(connection, city):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM candidates WHERE city = ?",
        (city,)
    )
    return cursor.fetchall()

def find_candidate_by_name(connection, name):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM candidates WHERE name = ?",
        (name,)
    )
    return cursor.fetchone()


