import unittest
import pandas as pd
import numpy as np
from ..plugins.date_plugin import DateValidator
from scripts.common import MISSING_VALUE_STRINGS

class TestDateValidator(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Med_ID': range(1, 11),
            'Visit_ID': [1] * 10,
            'valid_dates': ['01/2020', '02/2020', '03/2020', '04/2020', '05/2020',
                          '06/2020', '07/2020', '08/2020', '09/2020', '10/2020'],
            'invalid_dates': ['2020/01', '2020-02', '03-2020', 'Apr 2020', '05/20',
                           '06.2020', '07/01/2020', '08/2020', '09/2020', '10/2020'],
            'with_nulls': ['01/2020', '02/2020', None, '04/2020', np.nan,
                         '06/2020', '07/2020', '08/2020', '09/2020', '10/2020'],
            'with_missing': ['01/2020', '02/2020', '-9999', '04/2020', '-8888',
                          '06/2020', '07/2020', '08/2020', '09/2020', '10/2020'],
            'ymd_dates': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01',
                        '2020-05-01', '2020-06-01', '2020-07-01', '2020-08-01',
                        '2020-09-01', '2020-10-01']
        })
        self.validator = DateValidator()
        
    def test_valid_date_format(self):
        """Test that correctly formatted dates are not flagged"""
        flagged = self.validator.validate(self.df, 'valid_dates', None)
        self.assertEqual(len(flagged), 0)

    def test_invalid_date_format(self):
        """Test that incorrectly formatted dates are flagged"""
        flagged = self.validator.validate(self.df, 'invalid_dates', None)
        # First 7 dates are invalid for %m/%Y format
        self.assertEqual(len(flagged), 7)
        for f in flagged:
            self.assertTrue('Date Format Mismatch' in f.method)

    def test_null_handling(self):
        """Test that null values are properly excluded"""
        flagged = self.validator.validate(self.df, 'with_nulls', None)
        self.assertTrue(all(not pd.isna(f.value) for f in flagged))
        self.assertTrue(all(f.value not in [None, np.nan] for f in flagged))

    def test_missing_value_handling(self):
        """Test that missing value codes are properly excluded"""
        flagged = self.validator.validate(self.df, 'with_missing', None)
        self.assertTrue(all(str(f.value) not in MISSING_VALUE_STRINGS for f in flagged))

    def test_custom_format(self):
        """Test that custom date formats work correctly"""
        validator_ymd = DateValidator(expected_format='%Y-%m-%d')
        flagged = validator_ymd.validate(self.df, 'ymd_dates', None)
        self.assertEqual(len(flagged), 0)

        # Test with invalid format for these dates
        validator_mdy = DateValidator(expected_format='%m/%d/%Y')
        flagged = validator_mdy.validate(self.df, 'ymd_dates', None)
        self.assertEqual(len(flagged), 10)

    def test_invalid_column(self):
        """Test handling of nonexistent columns"""
        flagged = self.validator.validate(self.df, 'nonexistent_column', None)
        self.assertEqual(len(flagged), 0)

    def test_metadata_capture(self):
        """Test that all metadata is properly captured in flagged values"""
        flagged = self.validator.validate(self.df, 'invalid_dates', None)
        self.assertTrue(len(flagged) > 0)
        
        flagged_value = flagged[0]
        self.assertIsNotNone(flagged_value.med_id)
        self.assertIsNotNone(flagged_value.visit_id)
        self.assertEqual(flagged_value.column, 'invalid_dates')
        self.assertIsNotNone(flagged_value.value)
        self.assertTrue('Date Format Mismatch' in flagged_value.method)

    def test_empty_strings(self):
        """Test handling of empty strings"""
        df_with_empty = self.df.copy()
        df_with_empty['valid_dates'] = df_with_empty['valid_dates'].replace('01/2020', '')
        flagged = self.validator.validate(df_with_empty, 'valid_dates', None)
        self.assertEqual(len(flagged), 0, "Empty strings should be treated as missing values")

    def test_error_handling(self):
        """Test that validation errors are handled gracefully"""
        # Create a column with mixed types
        df_mixed = self.df.copy()
        df_mixed['mixed_types'] = ['01/2020', 2, '03/2020', True, '05/2020',
                                 '06/2020', '07/2020', '08/2020', '09/2020', '10/2020']
        flagged = self.validator.validate(df_mixed, 'mixed_types', None)
        self.assertTrue(any('Date Format Mismatch' in f.method for f in flagged))

if __name__ == '__main__':
    unittest.main()