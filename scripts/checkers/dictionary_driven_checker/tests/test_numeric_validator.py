import unittest
import pandas as pd
import numpy as np
from ..plugins.numeric_plugin import NumericValidator, NumericValidationError
from scripts.common import OutlierMethod

class TestNumericValidator(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Med_ID': range(1, 11),
            'Visit_ID': [1] * 10,
            'normal_dist': np.random.normal(100, 10, 10),
            'with_outliers': [1, 2, 3, 4, 5, 100, 2, 3, 4, 5],
            'binary': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            'small_range': range(1, 11),
            'with_nulls': [1, 2, None, 4, np.nan, 6, 7, 8, 9, 10],
            'missing_codes': [1, 2, -9999, 4, -8888, 6, 7, 8, 9, 10],
            'all_same': [5] * 10,
            'sparse_binary': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        })
        
    def test_outlier_detection_iqr(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'with_outliers', None)
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0].value, 100)
        self.assertTrue(flagged[0].method.startswith('IQR Outlier'))

    def test_outlier_detection_std(self):
        validator = NumericValidator(OutlierMethod.STD)
        flagged = validator.validate(self.df, 'with_outliers', None)
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0].value, 100)
        self.assertTrue(flagged[0].method.startswith('STD Outlier'))

    def test_binary_column(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'binary', None)
        self.assertEqual(len(flagged), 0, "Binary columns should not be flagged")

    def test_sparse_binary(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'sparse_binary', None)
        self.assertEqual(len(flagged), 0, "Sparse binary columns should not be flagged")

    def test_small_range(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'small_range', None)
        self.assertEqual(len(flagged), 0, "Small range columns should not be flagged")

    def test_constant_column(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'all_same', None)
        self.assertEqual(len(flagged), 0, "Constant columns should not be flagged")

    def test_range_validation(self):
        validator = NumericValidator(OutlierMethod.IQR)
        ranges = {(0, 50)}
        flagged = validator.validate(self.df, 'with_outliers', ranges)
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0].value, 100)
        self.assertEqual(flagged[0].method, "Outside defined range")

    def test_multiple_ranges(self):
        validator = NumericValidator(OutlierMethod.IQR)
        ranges = {(0, 10), (90, 110)}  # Two valid ranges
        flagged = validator.validate(self.df, 'with_outliers', ranges)
        self.assertEqual(len(flagged), 0, "Value 100 should be valid in second range")

    def test_null_handling(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'with_nulls', None)
        self.assertTrue(all(not pd.isna(f.value) for f in flagged), 
                       "Null values should be excluded from outlier detection")

    def test_missing_code_handling(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'missing_codes', None)
        self.assertTrue(all(f.value not in [-9999, -8888] for f in flagged),
                       "Missing value codes should be excluded")

    def test_invalid_column(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'nonexistent_column', None)
        self.assertEqual(len(flagged), 0, "Invalid columns should return empty list")

    def test_metadata_capture(self):
        validator = NumericValidator(OutlierMethod.IQR)
        flagged = validator.validate(self.df, 'with_outliers', None)
        self.assertEqual(len(flagged), 1)
        
        # Verify all metadata is captured
        flagged_value = flagged[0]
        self.assertIsNotNone(flagged_value.med_id)
        self.assertIsNotNone(flagged_value.visit_id)
        self.assertEqual(flagged_value.column, 'with_outliers')
        self.assertEqual(flagged_value.value, 100)
        self.assertTrue('IQR Outlier' in flagged_value.method)

if __name__ == '__main__':
    unittest.main()