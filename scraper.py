import psycopg2
import fighter
from bs4 import BeautifulSoup
from urllib import request
from geopy.geocoders import Nominatim
from multiprocessing import Process
from config_mapper import ConfigParse

weight_classes = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light_Heavyweight', 'Heavyweight', 'Women_Strawweight', 'Women_Flyweight', 'Women_Bantamweight', 'Women_Featherweight']
fighters_list = []

# Create a parsed config object referencing your config 
config = ConfigParse('config.ini')
database_name = config.ConfigSectionMap('database_info')['database_name']
database_user = config.ConfigSectionMap('database_info')['username']
database_pw = config.ConfigSectionMap('database_info')['password']
table_name = config.ConfigSectionMap('database_info')['table_name']

# Connect to postgres DB
conn = psycopg2.connect(dbname=database_name, user=database_user, password=database_pw)
cursor = conn.cursor()
weight_classes = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light_Heavyweight', 'Heavyweight', 'Women_Strawweight', 'Women_Flyweight', 'Women_Bantamweight', 'Women_Featherweight']
sql = """INSERT INTO %s(name, birthplace, age, height, weight, weight_class, reach, record, latitude, longitude)
         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         ON CONFLICT ON CONSTRAINT unique_fighter_weight DO UPDATE
         SET birthplace = %s, age = %s, height = %s, reach = %s, record = %s  
            """


def write_fighter_to_db(conn, cursor, fighter):
    """Insert fighter into database (or update)."""

    try:
        print(fighter.name)
        cursor.execute(sql % (table_name), (fighter.name, fighter.location, fighter.age, fighter.height, fighter.weight, fighter.weight_class, fighter.reach, fighter.record, fighter.lat, fighter.long, fighter.location, fighter.age, fighter.height, fighter.reach, fighter.record))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_webpage(url):
    """Open webpage and return decoded page."""

    web_page_request = request.urlopen(url)
    bytecode = web_page_request.read()
    html_doc = bytecode.decode()
    return html_doc

def find_fighter_page(parsed_html, weight_class_in):
    """Search parsed html page and find all instances of a fighter."""

    for fighter in parsed_html.find_all(class_='fighter-info'):
        if(type(fighter.find('a')) is not type(None)):
            fighter_url = 'http://www.ufc.com/' + fighter.find('a').get('href')
            fighter_doc = get_webpage(fighter_url)
            fighter_doc_parsed = BeautifulSoup(fighter_doc, 'html.parser')
            find_fighter_info(fighter_doc_parsed, weight_class_in)

def find_single_fighter(fighter_url, weight_class_in):
    """Take fighter page url and parse the page for info."""

    fighter_doc = get_webpage(fighter_url)
    fighter_doc_parsed = BeautifulSoup(fighter_doc, 'html.parser')
    find_fighter_info(fighter_doc_parsed, weight_class)

def find_fighter_info(parsed_fighter_html, weight_class_in):
    global fighters_list
    """Find info on page and create a fighter object."""

    name = parsed_fighter_html.title.text
    name = name.split('- ')[0].split('-Official')[0].strip()

    try:
        location = parsed_fighter_html.find(id='fighter-from').text.strip()
    except AttributeError:
        location = 'Not Available'
    location = ' '.join(location.split())

    try:
        age = parsed_fighter_html.find(id='fighter-age').text.strip()
    except AttributeError:
        age = 0

    try:
        height = parsed_fighter_html.find(id='fighter-height').text.strip()
    except AttributeError:
        height = 'Not Available'

    try:
        weight = parsed_fighter_html.find(id='fighter-weight').text.strip()
    except AttributeError:
        weight = 'Not Available'

    try:
        reach = parsed_fighter_html.find(id='fighter-reach').text.strip()
    except AttributeError:
        reach = 'Not Available'

    try:
        record = parsed_fighter_html.find(id='fighter-skill-record').text.strip()
    except AttributeError:
        record = 'Not Available'
    new_fighter = fighter.Fighter(name, location, age, height, weight, weight_class_in, reach, record)
    fighters_list.append(new_fighter)

def get_fighter_process(weight_class):
    base_url = 'http://www.ufc.com//fighter/Weight_Class/filterFighters?weightClass=' + weight_class + '&fighterFilter=Current'
    html_document = get_webpage(base_url)
    soup = BeautifulSoup(html_document, 'html.parser')

    if soup.find(class_='pagination'):
        for page in soup.find(class_='pagination').find_all('a'):
            page_url = 'http://www.ufc.com/' + page.get('href')
            temp_doc = get_webpage(page_url)
            temp_doc_soup = BeautifulSoup(temp_doc, 'html.parser')
            find_fighter_page(temp_doc_soup, weight_class)
    else:
        temp_doc = get_webpage(page_url)
        temp_doc_soup = BeautifulSoup(temp_doc, 'html.parser')
        find_fighter_page(temp_doc_soup, weight_class)

def main():
    global fighters_list
    procs = []

    for weight_class in weight_classes:
        proc = Process(target=get_fighter_process, args=(weight_class,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    print('Fighters list{}'.format(fighters_list))
    print("before db write")
    for fighter in fighters_list:
        print("in db write")
        write_fighter_to_db(conn, cursor, fighter)
    print("after db write")
    conn.close()

if __name__ == '__main__':
    main()