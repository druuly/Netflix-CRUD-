# task: create tables for account and content, then a junction table between the two

import sqlite3

# connect to library db, used in previous project
def setup_database():
    conn = sqlite3.connect("library_system.db")
    cursor = conn.cursor()

    # clean previous data
    # drop from least to most important. avoids foreign key errors
    print("Cleaning up old data...")
    cursor.execute("DROP TABLE IF EXISTS Account")
    cursor.execute("DROP TABLE IF EXISTS Content")
    cursor.execute("DROP TABLE IF EXISTS Content_person")

    # create new tables
    print("Creating new tables...")
    cursor.execute('''CREATE TABLE Account(
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR NOT NULL UNIQUE,
                password_hash VARCHAR,
                created_at DATETIME,
                account_status VARCHAR,
                country_code VARCHAR,
                preferred_language VARCHAR,
                plan_id INTEGER,
                FOREIGN KEY (plan_id) REFERENCES Subscription_Plan(plan_id)
                )''')
    
    cursor.execute('''CREATE TABLE Content(
                content_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR,
                content_type VARCHAR,
                release_year YEAR,
                content_link VARCHAR,
                maturity_rating FLOAT,
                description VARCHAR,
                duration_mins INTEGER,
                is_original BOOLEAN,
                studio_id INTEGER,
                FOREIGN KEY (studio_id) REFERENCES Studio (studio_id)
                )''')
    
    cursor.execute('''CREATE TABLE Content_person(
                content_id INTEGER,
                person_id INTEGER,
                role_type VARCHAR,
                director VARCHAR,
                PRIMARY KEY (content_id, person_id),
                FOREIGN KEY (content_id) REFERENCES Content(content_id),
                FOREIGN KEY (person_id) REFERENCES Person(person_id)
                )''')
    
    # plant seed data w/ tuples
    print("Seeding data...")
    account_data = [
        ('oscareucedaf1@gmail.com' , '1,2,3,4,5'),
        ('test@gmail.com' , "testpassword123"),
        ('tester@gmail.com' , "testpassword123")
    ]

    cursor.executemany("INSERT INTO Account (email, password_hash) VALUES (?,?)" , account_data)

    content_data = [
        ("The Sopranos" , "Crime" , 1999 , "https://youtu.be/JzKpfBK4Noo"),
        ("Breaking Bad" , "Crime" , 2008 , "https://youtu.be/T3x1tzOuXbQ"),
        ("No Country For Old Men" , "Western" , 2007 , "https://youtu.be/opbi7d42s8E")
    ]

    cursor.executemany("INSERT INTO Content (title, content_type, release_year, content_link) VALUES (? , ? , ? , ?)" , content_data)

    content_person_data = [
        ("director" , "Quentin Tarantino"),
        ("member" , "Mrs. Plankton")]

    cursor.executemany("INSERT INTO Content_person (role_type, director) VALUES (? , ?)" , content_person_data)

    conn.commit()
    conn.close()
    print("Database is refreshed and ready.")

if __name__ == "__main__":
    setup_database()