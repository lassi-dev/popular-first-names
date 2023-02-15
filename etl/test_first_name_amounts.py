import unittest
import first_name_amounts as fna
import copy
import datetime
import time
import pandas

class TestFirstNameAmounts(unittest.TestCase):

    template = {'YEAR_OF_BIRTH': '1969',
                'BIRTH_MUNICIPALITY_NUMBER': '049',
                'BIRTH_MUNICIPALITY_NAME': 'Espoo',
                'GENDER': '1',
                'FIRST_NAME': 'Mika',
                'AMOUNT': '39'}

    template_mu = pandas.DataFrame([{'ID': 1,
                                    'MUNICIPALITY_NUMBER': 49,
                                    'MUNICIPALITY_NAME_FI': 'Espoo'},
                                    {'ID': 2,
                                    'MUNICIPALITY_NUMBER': 50,
                                    'MUNICIPALITY_NAME_FI': 'Helsinki'}])

    def test_FirstNameAmounts(self):
        fna.FirstNameAmounts(1)

    def test_transform(self):
        fna.FirstNameAmounts(1).transform(self.template)

    def test_transform_returns_dict(self):
        self.assertIsInstance(fna.FirstNameAmounts(1).transform(self.template), dict)

    def test_transform_first_name_doesnt_change(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        self.assertEqual(result['FIRST_NAME'], 'Mika')

    def test_transform_year_of_birth_to_number(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        self.assertEqual(result['YEAR_OF_BIRTH'], 1969)

    def test_transform_year_of_birth_if_None_equal_negative(self):
        fina = fna.FirstNameAmounts(1)
        mod_template = copy.deepcopy(self.template)
        mod_template['YEAR_OF_BIRTH'] = None
        result = fina.transform(mod_template)
        self.assertEqual(result['YEAR_OF_BIRTH'], -1)

    def test_transform_doesnt_modify_original(self):
        fina = fna.FirstNameAmounts(1)
        fina.transform(self.template)
        self.assertEqual(self.template['YEAR_OF_BIRTH'], '1969')

    def test_transform_amount_to_number(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        self.assertEqual(result['AMOUNT'], 39)

    def test_transform_amount_if_None_equal_0(self):
        fina = fna.FirstNameAmounts(1)
        mod_template = copy.deepcopy(self.template)
        mod_template['AMOUNT'] = None
        result = fina.transform(mod_template)
        self.assertEqual(result['AMOUNT'], 0)

    def test_transform_gender_1_to_male(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        self.assertEqual(result['GENDER'], 'Mies')

    def test_transform_gender_2_to_female(self):
        mod_template = copy.deepcopy(self.template)
        mod_template['GENDER'] = '2'
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(mod_template)
        self.assertEqual(result['GENDER'], 'Nainen')

    def test_transform_gender_None_to_unknown(self):
        mod_template = copy.deepcopy(self.template)
        mod_template['GENDER'] = None
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(mod_template)
        self.assertEqual(result['GENDER'], 'Tuntematon')

    def test_transform_gender_other_to_unknown(self):
        mod_template = copy.deepcopy(self.template)
        mod_template['GENDER'] = '12'
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(mod_template)
        self.assertEqual(result['GENDER'], 'Tuntematon')

    def test_transform_id_added(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        self.assertEqual(result['ID'], 1)

    def test_transform_ids_increment(self):
        fina = fna.FirstNameAmounts(1)
        fina.transform(self.template)
        result = fina.transform(self.template)
        self.assertEqual(result['ID'], 2)

    def test_transform_load_date_added(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        result['LOAD_DATE']

    def test_transform_load_date_is_datetime(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        self.assertIsInstance(result['LOAD_DATE'], datetime.datetime)

    def test_transform_load_date_is_same_for_two(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        time.sleep(0.1)
        result2 = fina.transform(self.template)
        self.assertEqual(result['LOAD_DATE'], result2['LOAD_DATE'])

    def test_transform_municipality_id(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        result['MUNICIPALITY_ID']

    def test_transform_municipality_id_municipalities_not_set_return_None(self):
        fina = fna.FirstNameAmounts(1)
        result = fina.transform(self.template)
        self.assertEqual(result['MUNICIPALITY_ID'], None)

    def test_transform_municipality_id_set_municipalities(self):
        municipalities = self.template_mu
        fna.FirstNameAmounts(1).setMunicipalities(municipalities)

    def test_transform_municipality_id_return_id_by_mun_number(self):
        municipalities = self.template_mu
        fina = fna.FirstNameAmounts(1)
        fina.setMunicipalities(municipalities)
        result = fina.transform(self.template)
        self.assertEqual(result['MUNICIPALITY_ID'], 1)

    def test_transform_municipality_id_return_id_by_different_mun_number(self):
        municipalities = self.template_mu
        mod_tempalte = copy.deepcopy(self.template)
        mod_tempalte['BIRTH_MUNICIPALITY_NUMBER'] = '050'

        fina = fna.FirstNameAmounts(1)
        fina.setMunicipalities(municipalities)
        result = fina.transform(mod_tempalte)

        self.assertEqual(result['MUNICIPALITY_ID'], 2)

    def test_transform_municipality_id_return_id_by_different_mun_number_but_municipalities_modified(self):
        municipalities = copy.deepcopy(self.template_mu)
        municipalities.loc[municipalities['MUNICIPALITY_NUMBER'] == 49,'ID'] = 3

        fina = fna.FirstNameAmounts(1)
        fina.setMunicipalities(municipalities)
        result = fina.transform(self.template)
        
        self.assertEqual(result['MUNICIPALITY_ID'], 3)

    def test_transform_municipality_id_if_number_is_None_use_name(self):
        mod_template = copy.deepcopy(self.template)
        mod_template['BIRTH_MUNICIPALITY_NUMBER'] = None

        fina = fna.FirstNameAmounts(1)
        fina.setMunicipalities(self.template_mu)
        result = fina.transform(mod_template)
        self.assertEqual(result['MUNICIPALITY_ID'], 1)

    def test_transform_municipality_id_if_number_is_not_in_municipalities_use_name(self):
        mod_template = copy.deepcopy(self.template)
        mod_template['BIRTH_MUNICIPALITY_NUMBER'] = '123'

        fina = fna.FirstNameAmounts(1)
        fina.setMunicipalities(self.template_mu)
        result = fina.transform(mod_template)
        self.assertEqual(result['MUNICIPALITY_ID'], 1)

    def test_transform_municipality_id_if_number_and_name_are_None_return_None(self):
        mod_template = copy.deepcopy(self.template)
        mod_template['BIRTH_MUNICIPALITY_NUMBER'] = None
        mod_template['BIRTH_MUNICIPALITY_NAME'] = None

        fina = fna.FirstNameAmounts(1)
        fina.setMunicipalities(self.template_mu)
        result = fina.transform(mod_template)
        self.assertEqual(result['MUNICIPALITY_ID'], None)


    def test_transformDataFrame(self):
        fina = fna.FirstNameAmounts(1)
        df = pandas.DataFrame([self.template])
        fina.transformDataFrame(df)

    def test_transformDataFrame_returns_DataFrame(self):
        fina = fna.FirstNameAmounts(1)
        df = pandas.DataFrame([self.template])
        self.assertIsInstance(fina.transformDataFrame(df),pandas.DataFrame)

    def test_transformDataFrame_id_equal_result_of_transfrom(self):
        fina_tst = fna.FirstNameAmounts(1)
        df_tst = fina_tst.transform(self.template)
       
        fina = fna.FirstNameAmounts(1)
        df = pandas.DataFrame([self.template])
        result = fina.transformDataFrame(df)
        self.assertEqual(result.iloc[0]['ID'], df_tst['ID'])

    def test_transformDataFrame_multiple_ids_equal_result_of_transfrom(self):
        fina_tst = fna.FirstNameAmounts(1)
        df_tst = fina_tst.transform(self.template)
        value = copy.deepcopy(self.template)
        df_tst2 = fina_tst.transform(value)
       
        fina = fna.FirstNameAmounts(1)
        df = pandas.DataFrame([self.template, value])
        result = fina.transformDataFrame(df)
        self.assertEqual(result.iloc[0]['ID'], df_tst['ID'])
        self.assertEqual(result.iloc[1]['ID'], df_tst2['ID'])

    def test_transformDataFrame_multiple_municipality_ids_equal_result_of_transfrom(self):
        fina_tst = fna.FirstNameAmounts(1)
        fina_tst.setMunicipalities(self.template_mu)

        df_tst = fina_tst.transform(self.template)
        value = copy.deepcopy(self.template)
        value['BIRTH_MUNICIPALITY_NUMBER'] = '050'
        df_tst2 = fina_tst.transform(value)
       
        fina = fna.FirstNameAmounts(1)
        fina.setMunicipalities(self.template_mu)

        df = pandas.DataFrame([self.template, value])
        result = fina.transformDataFrame(df)

        self.assertEqual(result.iloc[0]['MUNICIPALITY_ID'], df_tst['MUNICIPALITY_ID'])
        self.assertEqual(result.iloc[1]['MUNICIPALITY_ID'], df_tst2['MUNICIPALITY_ID'])

    def test_transformDataFrame_no_row_where_name_is_None_returned(self):
        fina = fna.FirstNameAmounts(1)

        value = copy.deepcopy(self.template)
        value['FIRST_NAME'] = None

        df = pandas.DataFrame([self.template, value])
        result = fina.transformDataFrame(df)
        self.assertFalse(result['FIRST_NAME'].isnull().values.any())
        self.assertTrue(len(result) == 1)
