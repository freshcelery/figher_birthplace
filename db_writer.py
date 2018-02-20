import psycopg2

# Connect to postgres DB
conn = psycopg2.connect(dbname='fighters', user='fighters', password='Zone10%%')
cursor = conn.cursor()
weight_classes = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light_Heavyweight', 'Heavyweight', 'Women_Strawweight', 'Women_Flyweight', 'Women_Bantamweight', 'Women_Featherweight']
flyweight_sql = """INSERT INTO flyweight_fighter(name, birthplace, age, height, weight, reach, record, latitude, longitude)
         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
         ON CONFLICT ON CONSTRAINT unique_fighter_weight DO UPDATE
         SET birthplace = %s, age = %s, height = %s, reach = %s, record = %s  
            """

bantamweight_sql = """INSERT INTO flyweight_fighter(name, birthplace, age, height, weight, reach, record, latitude, longitude)
         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
         ON CONFLICT ON CONSTRAINT unique_fighter_weight DO UPDATE
         SET birthplace = %s, age = %s, height = %s, reach = %s, record = %s  
            """

featherweight_sql = """INSERT INTO flyweight_fighter(name, birthplace, age, height, weight, reach, record, latitude, longitude)
         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
         ON CONFLICT ON CONSTRAINT unique_fighter_weight DO UPDATE
         SET birthplace = %s, age = %s, height = %s, reach = %s, record = %s  
            """


def write_fighter_to_db(conn, cursor, fighter):
    """Insert fighter into database (or update)."""


    try:
        cursor.execute(flyweight_sql, (fighter.name, fighter.location, fighter.age, fighter.height, fighter.weight, fighter.reach, fighter.record, fighter.lat, fighter.long, fighter.location, fighter.age, fighter.height, fighter.reach, fighter.record))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)