import fighter
import psycopg2
from geopy.geocoders import Nominatim
from config_mapper import ConfigParse

# Create a parsed config object referencing your config 
config = ConfigParse('config.ini')
database_name = config.ConfigSectionMap('database_info')['database_name']
database_user = config.ConfigSectionMap('database_info')['username']
database_pw = config.ConfigSectionMap('database_info')['password']
table_name = config.ConfigSectionMap('database_info')['table_name']

get_sql = """
    SELECT * FROM %s WHERE (latitude = '0' and longitude = '0')
    OR (latitude IS NULL and longitude IS NULL); 
"""

update_sql = """
    UPDATE %s
    SET latitude = %s, longitude = %s
    WHERE name LIKE %s;
"""

def main():

    conn = psycopg2.connect(dbname=database_name, user=database_user, password=database_pw)
    cursor = conn.cursor()

    geolocator = Nominatim()

    try:
        cursor.execute(get_sql % (table_name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


    sql_results = cursor.fetchall()

    for result in sql_results:
        name = result[1]
        birthplace = result[2]

        try:
            location = geolocator.geocode(birthplace)
            cursor.execute(update_sql % (table_name), (location.latitude, location.longitude, name))
            conn.commit()
        except:
            print('FAILED! Name: {}, Birthplace: {}'.format(name, birthplace))

    conn.close()

if __name__ == '__main__':
    main()