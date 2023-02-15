import unittest
import municipalities as mun
import copy
import datetime
import time
import pandas

class TestMunicipalities(unittest.TestCase):

    template = {'MUNICIPALITY_NUMBER': 5
                , 'MUNICIPALITY_NAME_FI': 'Alajärvi'
                , 'MUNICIPALITY_NAME_SE': 'Alajärvi'
                , 'MUNICIPALITY_TYPE': 'Kaupunki'
                , 'PRIMARY_LANGUAGE': 'suomi'
                , 'ELECTORAL_DISTRICT_NUMBER': 10
                , 'ELECTORAL_DISTRICT_NAME_FI': 'Vaasan vaalipiiri'
                , 'ELECTORAL_DISTRICT_NAME_SE': 'Vasa valkrets'
                , 'REGION_NUMBER': 13
                , 'REGION_NAME_FI': 'Etelä-Pohjanmaa'
                , 'REGION_NAME_SE': 'Södra Österbotten'
                }

    def test_Municipalities(self):
        mun.Municipalities(1)

    def test_transform(self):
        mu = mun.Municipalities(1)
        mu.transform(self.template)

    def test_transform_returns_dict(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertIsInstance(result, dict)

    def test_transform_municipality_number_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['MUNICIPALITY_NUMBER'], 5)

    def test_transform_municipality_name_fi_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['MUNICIPALITY_NAME_FI'], 'Alajärvi')

    def test_transform_municipality_name_se_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['MUNICIPALITY_NAME_SE'], 'Alajärvi')

    def test_transform_municipality_type_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['MUNICIPALITY_TYPE'], 'Kaupunki')

    def test_transform_primary_language_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['PRIMARY_LANGUAGE'], 'suomi')

    def test_transform_electoral_district_number_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['ELECTORAL_DISTRICT_NUMBER'], 10)

    def test_transform_electoral_district_name_fi_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['ELECTORAL_DISTRICT_NAME_FI'], 'Vaasan vaalipiiri')

    def test_transform_electoral_district_name_se_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['ELECTORAL_DISTRICT_NAME_SE'], 'Vasa valkrets')

    def test_transform_region_number_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['REGION_NUMBER'], 13)

    def test_transform_region_name_fi_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['REGION_NAME_FI'], 'Etelä-Pohjanmaa')

    def test_transform_region_name_se_doesnt_change(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['REGION_NAME_SE'], 'Södra Österbotten')

    def test_transform_id_added(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertEqual(result['ID'], 1)

    def test_transform_ids_increment(self):
        mu = mun.Municipalities(1)
        mu.transform(self.template)
        result = mu.transform(self.template)
        self.assertEqual(result['ID'], 2)

    def test_transform_doesnt_modify_original(self):
        mu = mun.Municipalities(1)
        mu.transform(self.template)
        with self.assertRaises(KeyError):
            self.template['ID']

    def test_transform_load_date_added(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        result['LOAD_DATE']

    def test_transform_load_date_is_datetime(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        self.assertIsInstance(result['LOAD_DATE'], datetime.datetime)

    def test_transform_load_date_is_same_for_two(self):
        mu = mun.Municipalities(1)
        result = mu.transform(self.template)
        time.sleep(0.1)
        result2 = mu.transform(self.template)
        self.assertEqual(result['LOAD_DATE'], result2['LOAD_DATE'])

    def test_transformDataFrame(self):
        mu = mun.Municipalities(1)
        df = pandas.DataFrame()
        mu.transformDataFrame(df)

    def test_transformDataFrame_returns_DataFrame(self):
        mu = mun.Municipalities(1)
        df = pandas.DataFrame()
        self.assertIsInstance(mu.transformDataFrame(df),pandas.DataFrame)

    def test_transformDataFrame_id_equal_result_of_transfrom(self):
        mu_tst = mun.Municipalities(1)
        df_tst = mu_tst.transform(self.template)
       
        mu = mun.Municipalities(1)
        df = pandas.DataFrame([self.template])
        result = mu.transformDataFrame(df)
        self.assertEqual(result.iloc[0]['ID'], df_tst['ID'])

    def test_transformDataFrame_multiple_ids_equal_result_of_transfrom(self):
        mu_tst = mun.Municipalities(1)
        df_tst = mu_tst.transform(self.template)
        value = copy.deepcopy(self.template)
        df_tst2 = mu_tst.transform(value)
       
        mu = mun.Municipalities(1)
        df = pandas.DataFrame([self.template, value])
        result = mu.transformDataFrame(df)
        self.assertEqual(result.iloc[0]['ID'], df_tst['ID'])
        self.assertEqual(result.iloc[1]['ID'], df_tst2['ID'])

    def test_transformDataFrame_multiple_region_numbers_equal_result_of_transfrom(self):
        mu_tst = mun.Municipalities(1)
        df_tst = mu_tst.transform(self.template)
        value = copy.deepcopy(self.template)
        value['REGION_NUMBER'] = 14
        df_tst2 = mu_tst.transform(value)
       
        mu = mun.Municipalities(1)
        df = pandas.DataFrame([self.template, value])
        result = mu.transformDataFrame(df)
        self.assertEqual(result.iloc[0]['REGION_NUMBER'], df_tst['REGION_NUMBER'])
        self.assertEqual(result.iloc[1]['REGION_NUMBER'], df_tst2['REGION_NUMBER'])
