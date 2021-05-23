from datasource import Postgres
from config import Config
from datetime import datetime


sql = '''
select count(*) from %s
'''
tables = [
    'otodom',
    'morizon'
    ]
def counter():

    db = Postgres(Config.DSN)

    for t in tables:
        count = db.dict_select(f'select count(*) from {t}')
        file_path = '/home/noxiss/Projects/scrapers/oferty_mieszkan/counter.txt'
        print(file_path)
        with open(file_path, 'a+') as f:
            print(count)
            f.writelines(f"{datetime.now()} {t}: {count[0]['count']}\n")

if __name__ == '__main__':
    counter()
