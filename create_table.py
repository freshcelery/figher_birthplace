import psycopg2
from config_mapper import ConfigParse

# Create a parsed config object referencing your config 
config = ConfigParse('config.ini')
database_name = config.ConfigSectionMap('database_info')['database_name']
database_user = config.ConfigSectionMap('database_info')['username']
database_pw = config.ConfigSectionMap('database_info')['password']
table_name = config.ConfigSectionMap('database_info')['table_name']

create_table_sql = """
    CREATE TABLE "%s" (
        id integer DEFAULT nextval('fighter_id_seq_2') PRIMARY KEY,
        name character varying(100),
        birthplace character varying(100),
        age integer,
        height character varying(20),
        weight character varying(20),
        reach character varying(20),
        record character varying(20),
        latitude double precision,
        longitude double precision,
        weight_class character varying(50),
        CONSTRAINT unique_fighter_weight_2 UNIQUE (name, weight)
    );
"""

create_sequence_sql = """
    CREATE SEQUENCE fighter_id_seq_2
        AS integer
        START WITH 1
        INCREMENT BY 1
        NO MINVALUE
        NO MAXVALUE
        CACHE 1;
"""


def main():

    conn = psycopg2.connect(dbname=database_name, user=database_user, password=database_pw)
    cursor = conn.cursor()


    try:
        cursor.execute(create_sequence_sql)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Creating sequence failed with error: {}'.format(error))

    try:
        cursor.execute(create_table_sql % (table_name))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Creating table failed with error: {}'.format(error))

    conn.close()

if __name__ == '__main__':
    main()