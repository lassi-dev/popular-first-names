import sqlite3
import pandas
import copy
import datetime
import municipalities
import jsonlines

class FirstNameAmounts:

    def __init__(self, IdStart: int) -> None:
        self.id = IdStart
        self.loadDate = datetime.datetime.now()
        self.municipalities = None

    def setMunicipalities(self, municipalities: pandas.DataFrame):
        self.municipalities = municipalities

    def transform(self, sourceDict: dict):
        result = copy.deepcopy(sourceDict)
        if result['YEAR_OF_BIRTH'] is None:
            result['YEAR_OF_BIRTH'] = -1
        else:
            result['YEAR_OF_BIRTH'] = int(result['YEAR_OF_BIRTH'])

        if result['AMOUNT'] is None:
            result['AMOUNT'] = 0
        else:
            result['AMOUNT'] = int(result['AMOUNT'])

        if result['GENDER'] == '1':
            result['GENDER'] = 'Mies'
        elif result['GENDER'] == '2':
            result['GENDER'] = 'Nainen'
        else:
            result['GENDER'] = 'Tuntematon'

        result['ID'] = self.id
        self.id = self.id + 1

        result['LOAD_DATE'] = self.loadDate

        if self.municipalities is not None:
            if result['BIRTH_MUNICIPALITY_NUMBER'] is None and result['BIRTH_MUNICIPALITY_NAME'] is None:
                result['MUNICIPALITY_ID'] = None
            elif result['BIRTH_MUNICIPALITY_NUMBER'] is None:
                result['MUNICIPALITY_ID'] = self.municipalities.loc[self.municipalities['MUNICIPALITY_NAME_FI'] == result['BIRTH_MUNICIPALITY_NAME']].ID.item()
            elif int(result['BIRTH_MUNICIPALITY_NUMBER']) not in self.municipalities['MUNICIPALITY_NUMBER'].values:
                result['MUNICIPALITY_ID'] = self.municipalities.loc[self.municipalities['MUNICIPALITY_NAME_FI'] == result['BIRTH_MUNICIPALITY_NAME']].ID.item()
            else:
                municipality_number = int(result['BIRTH_MUNICIPALITY_NUMBER'])
                result['MUNICIPALITY_ID'] = self.municipalities.loc[self.municipalities['MUNICIPALITY_NUMBER'] == municipality_number].ID.item()
        else:
            result['MUNICIPALITY_ID'] = None

        return result

    def transformDataFrame(self, df: pandas.DataFrame):

        di = df.to_dict('records')

        for i in range(0,len(di)):
            di[i] = self.transform(di[i])
        
        df = pandas.DataFrame(di) 
        df = df.dropna(subset=['FIRST_NAME'])

        return df


def persistsFirstNameAmounts(databaseName: str, df: pandas.DataFrame):
    fact = df.to_dict('records')
    conn = sqlite3.connect(databaseName)

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
                row['LOAD_DATE'].to_pydatetime()
            ))
    conn.commit()
    conn.close()

def etl_first_name_amounts(jsonlUrl: str, databaseName: str, municipalities: municipalities.Municipalities):
    fact = []
    with jsonlines.open(jsonlUrl) as reader:
        for row in reader:
            fact.append(row)

    df = pandas.DataFrame(fact)
    fna = FirstNameAmounts(1)
    fna.setMunicipalities(municipalities)
    df = fna.transformDataFrame(df)

    persistsFirstNameAmounts(databaseName, df)