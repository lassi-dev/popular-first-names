import municipalities
import first_name_amounts

parquetUrl = '../data/municipality-listing-2020-10-21.parquet'
jsonlUrl = '../data/most-popular-first-names-by-municipality.jsonl'
targetDB = '../first_name_amounts.sqlite'

municipalities.etl_municipalities(parquetUrl, targetDB)
first_name_amounts.etl_first_name_amounts(jsonlUrl, targetDB, municipalities.getMunicipalityIds(targetDB))