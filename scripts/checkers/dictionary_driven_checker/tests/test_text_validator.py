import unittest
import pandas as pd
import numpy as np
from ..plugins.text_plugin import TextValidator
from scripts.common import MISSING_VALUE_STRINGS

class TestTextValidator(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Med_ID': range(1, 11),
            'Visit_ID': [1] * 10,
            'common_values': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'],
            'rare_values': ['A', 'A', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            'with_nulls': ['A', 'B', None, 'C', np.nan, 'D', 'E', 'F', 'G', 'H'],
            'with_missing': ['A', 'B', '-9999', 'C', '-8888', 'D', 'E', 'F', 'G', 'H'],
            'all_same': ['A'] * 10,
            'with_spaces': [' A ', 'B ', ' C', ' D ', 'E', 'F', 'G', 'H', 'I', 'J']
        })
        self.validator = TextValidator()
        
    def test_rare_value_detection(self):
        """Test that values appearing less than threshold times are flagged"""
        flagged = self.validator.validate(self.df, 'rare_values', None)
        # B through H appear only once
        self.assertEqual(len(flagged), 7)
        flagged_values = {f.value for f in flagged}
        self.assertEqual(flagged_values, {'B', 'C', 'D', 'E', 'F', 'G', 'H'})

    def test_common_values(self):
        """Test that common values are not flagged"""
        flagged = self.validator.validate(self.df, 'common_values', None)
        self.assertEqual(len(flagged), 0)

    def test_null_handling(self):
        """Test that null values are properly excluded"""
        flagged = self.validator.validate(self.df, 'with_nulls', None)
        self.assertTrue(all(not pd.isna(f.value) for f in flagged))
        self.assertTrue(all(f.value not in [None, np.nan] for f in flagged))

    def test_missing_value_handling(self):
        """Test that missing value codes are properly excluded"""
        flagged = self.validator.validate(self.df, 'with_missing', None)
        self.assertTrue(all(str(f.value) not in MISSING_VALUE_STRINGS for f in flagged))

    def test_constant_column(self):
        """Test handling of columns with all same value"""
        flagged = self.validator.validate(self.df, 'all_same', None)
        self.assertEqual(len(flagged), 0)

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is handled properly"""
        flagged = self.validator.validate(self.df, 'with_spaces', None)
        self.assertTrue(all(not f.value.strip() in [v.strip() for v in self.df['with_spaces']] 
                          for f in flagged))

    def test_invalid_column(self):
        """Test handling of nonexistent columns"""
        flagged = self.validator.validate(self.df, 'nonexistent_column', None)
        self.assertEqual(len(flagged), 0)

    def test_metadata_capture(self):
        """Test that all metadata is properly captured in flagged values"""
        flagged = self.validator.validate(self.df, 'rare_values', None)
        self.assertTrue(len(flagged) > 0)
        
        flagged_value = flagged[0]
        self.assertIsNotNone(flagged_value.med_id)
        self.assertIsNotNone(flagged_value.visit_id)
        self.assertEqual(flagged_value.column, 'rare_values')
        self.assertIsNotNone(flagged_value.value)
        self.assertTrue('Rare Value' in flagged_value.method)

    def test_threshold_configuration(self):
        """Test that different thresholds work correctly"""
        validator_strict = TextValidator(rare_threshold=4)  # More strict
        flagged_strict = validator_strict.validate(self.df, 'rare_values', None)
        
        validator_lenient = TextValidator(rare_threshold=2)  # More lenient
        flagged_lenient = validator_lenient.validate(self.df, 'rare_values', None)
        
        self.assertTrue(len(flagged_strict) > len(flagged_lenient))

if __name__ == '__main__':
    unittest.main()