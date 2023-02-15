import copy
import datetime
import pandas
import sqlite3
import pyarrow.parquet as parquet

class Municipalities:

    def __init__(self, IdStart: int) -> None:
        self.id = IdStart
        self.loadDate = datetime.datetime.now()

    def transform(self, sourceDict: dict):
        result = copy.deepcopy(sourceDict)
        result['ID'] = self.id
        self.id = self.id + 1
        result['LOAD_DATE'] = self.loadDate
        return result

    def transformDataFrame(self, df: pandas.DataFrame):
        di = df.to_dict('records')

        for i in range(0,len(di)):
            di[i] = self.transform(di[i])

        return pandas.DataFrame(di)

def persistDataFrame(databaseName: str, df: pandas.DataFrame):
    municipalities = df.to_dict('records')
    conn = sqlite3.connect(databaseName)

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
                mp['LOAD_DATE'].to_pydatetime()
            ))
    conn.commit()
    conn.close()

def getMunicipalityIds(databaseName: str) -> pandas.DataFrame:
    conn = sqlite3.connect(databaseName)
    df = pandas.read_sql_query('''
                            select
                                  id
                                , municipality_number
                                , municipality_name_fi
                            from
                                municipalities
                            ;
                            ''', conn)
    df.columns = ['ID','MUNICIPALITY_NUMBER','MUNICIPALITY_NAME_FI']
    conn.close()
    return df

def etl_municipalities(pqUrl: str, databaseName: str):
    df = parquet.read_table(pqUrl).to_pandas()

    mu = Municipalities(1)
    df = mu.transformDataFrame(df)

    persistDataFrame(databaseName, df)