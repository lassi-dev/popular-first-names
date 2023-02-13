# The ETL code is copied into a python script so it can be run without the Jupyter Notebooks.

import pyarrow.parquet as parquet
import sqlite3
import datetime
import jsonlines
import pandas

parquetUrl = './data/municipality-listing-2020-10-21.parquet'
jsonlUrl = './data/most-popular-first-names-by-municipality.jsonl'

municipalities = parquet.read_table(parquetUrl).to_pylist()

for i in range(0,len(municipalities)):
    municipalities[i]['ID'] = i+1

loaddate = datetime.datetime.now()
for i in range(0,len(municipalities)):
    municipalities[i]['LOAD_DATE'] = loaddate

conn = sqlite3.connect('first_name_amounts.sqlite')

conn.execute('''
            drop table if exists municipalities;
            ''')
conn.execute('''
            create table municipalities (
            id integer primary key
            , municipality_number integer
            , municipality_name_fi text
            , municipality_name_se text
            , municipality_type text
            , primary_language text
            , electoral_district_number integer
            , electoral_district_name_fi text
            , electoral_district_name_se text
            , region_number integer
            , region_name_fi text
            , region_name_se text
            , load_date text
            );
            ''')

for mp in municipalities:
    conn.execute('''
        insert into municipalities (
        id
        , municipality_number
        , municipality_name_fi
        , municipality_name_se
        , municipality_type
        , primary_language
        , electoral_district_number
        , electoral_district_name_fi
        , electoral_district_name_se
        , region_number
        , region_name_fi
        , region_name_se
        , load_date
        ) values
        (?,?,?,?,?,?,?,?,?,?,?,?,?);
        ''',
        (
            mp['ID'],
            mp['MUNICIPALITY_NUMBER'],
            mp['MUNICIPALITY_NAME_FI'],
            mp['MUNICIPALITY_NAME_SE'],
            mp['MUNICIPALITY_TYPE'],
            mp['PRIMARY_LANGUAGE'],
            mp['ELECTORAL_DISTRICT_NUMBER'],
            mp['ELECTORAL_DISTRICT_NAME_FI'],
            mp['ELECTORAL_DISTRICT_NAME_SE'],
            mp['REGION_NUMBER'],
            mp['REGION_NAME_FI'],
            mp['REGION_NAME_SE'],
            mp['LOAD_DATE']
        ))
conn.commit()
conn.close()

fact = []
with jsonlines.open(jsonlUrl) as reader:
    for row in reader:
        fact.append(row)

for i in range(0,len(fact)):
    fact[i]['ID'] = i+1

def findMunicipalityIdbyName(municipality_name, municipalities):
    if(municipality_name is None):
        return -1
    mun_id = -1
    for row in municipalities:
        if row['MUNICIPALITY_NAME_FI'] == municipality_name:
            mun_id = row['ID']
    return mun_id

def findMunicipalityId(municipality_number, municipalities):
    if(municipality_number is None):
        return -1
    mun_id = -1
    for row in municipalities:
        if row['MUNICIPALITY_NUMBER'] == int(municipality_number):
            mun_id = row['ID']
    return mun_id

for row in fact:
    if row['BIRTH_MUNICIPALITY_NUMBER'] is None:
        row['MUNICIPALITY_ID'] = findMunicipalityIdbyName(row['BIRTH_MUNICIPALITY_NAME'], municipalities)
    else:
        row['MUNICIPALITY_ID'] = findMunicipalityId(row['BIRTH_MUNICIPALITY_NUMBER'], municipalities)

for row in fact:
    if row['MUNICIPALITY_ID'] == -1:
        row['MUNICIPALITY_ID'] = findMunicipalityIdbyName(row['BIRTH_MUNICIPALITY_NAME'], municipalities)

for row in fact:
    if row['GENDER'] == '1':
        row['GENDER'] = 'Mies'
    else:
        row['GENDER'] = 'Nainen'

df = pandas.DataFrame(fact)

df = df.dropna(subset=['FIRST_NAME'])

fact = df.to_dict('records')

loaddate = datetime.datetime.now()
for i in range(0,len(fact)):
    fact[i]['LOAD_DATE'] = loaddate

conn = sqlite3.connect('first_name_amounts.sqlite')

conn.execute('''
            drop table if exists first_name_amounts;
            ''')
conn.execute('''
            create table first_name_amounts (
                  id integer primary key
                , first_name text
                , gender text
                , municipality_id integer
                , year_of_birth integer
                , amount integer
                , load_date text
            );
            ''')

for row in fact:
    conn.execute('''
        insert into first_name_amounts (
              id
            , first_name
            , gender
            , municipality_id
            , year_of_birth
            , amount
            , load_date
        ) values
        (?,?,?,?,?,?,?);
        ''',
        (
            row['ID'],
            row['FIRST_NAME'],
            row['GENDER'],
            row['MUNICIPALITY_ID'],
            row['YEAR_OF_BIRTH'],
            row['AMOUNT'],
            row['LOAD_DATE']
        ))
conn.commit()
conn.close()