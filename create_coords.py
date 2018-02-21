from geopy.geocoders import Nominatim
import fighter
import psycopg2

# Create a parsed config object referencing your config 
config = ConfigParse('config.ini')
database_name = config.ConfigSectionMap('database_info')['database_name']
database_user = config.ConfigSectionMap('database_info')['username']
database_pw = config.ConfigSectionMap('database_info')['password']

def main():

    conn = psycopg2.connect(dbname=database_name, user=database_user, password=database_pw)
    cursor = conn.cursor()
    get_sql = """SELECT * FROM fighter WHERE latitude = '0' and longitude = '0';"""
    update_sql = """
                UPDATE fighter
                SET latitude = %s, longitude = %s
                WHERE name LIKE %s;
                 """

    geolocator = Nominatim()

    try:
        cursor.execute(get_sql)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


    sql_results = cursor.fetchall()

    for result in sql_results:
        name = result[1]
        birthplace = result[2]

        try:
            location = geolocator.geocode(birthplace)
            cursor.execute(update_sql, (location.latitude, location.longitude, name))
            conn.commit()
        except:
            print('FAILED! Name: {}, Birthplace: {}'.format(name, birthplace))

    conn.close()

if __name__ == '__main__':
    main()