import unittest
import pandas as pd
from pathlib import Path
import tempfile
from ..utils import run_dictionary_checker
from scripts.common import OutlierMethod

class TestDictionaryCheckerIntegration(unittest.TestCase):
    def setUp(self):
        # Create test dataset
        self.df = pd.DataFrame({
            'Med_ID': range(1, 11),
            'Visit_ID': [1] * 10,
            'numeric_normal': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'numeric_outliers': [1, 2, 3, 4, 5, 100, 2, 3, 4, 5],
            'text_normal': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'],
            'text_rare': ['A', 'A', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            'date_normal': ['01/2020', '02/2020', '03/2020', '04/2020', '05/2020',
                          '06/2020', '07/2020', '08/2020', '09/2020', '10/2020'],
            'date_invalid': ['2020/01', '2020-02', '03-2020', 'Apr 2020', '05/20',
                           '06.2020', '07/01/2020', '08/2020', '09/2020', '10/2020']
        })
        
        # Create test dictionary
        self.dict_df = pd.DataFrame({
            'Main Variable': ['numeric_normal', 'numeric_outliers', 'text_normal', 
                            'text_rare', 'date_normal', 'date_invalid'],
            'Type': ['numeric', 'numeric', 'text', 'text', 'date', 'date'],
            'Value': ['(0,10)', '(0,10)', '', '', '', ''],
            'Description': ['Test numeric', 'Test numeric with outliers', 
                          'Test text', 'Test text with rare values',
                          'Test dates', 'Test invalid dates']
        })
        
    def test_full_pipeline_iqr(self):
        """Test the complete dictionary checker pipeline using IQR method"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            output_path = Path(tmp.name)
            
            # Run the checker
            run_dictionary_checker(
                df=self.df,
                dict_df=self.dict_df,
                domain='TestDomain',
                output_path=output_path,
                outlier_method=OutlierMethod.IQR
            )
            
            # Read and validate results
            results = pd.read_csv(output_path)
            
            # Verify numeric outliers were caught
            numeric_flags = results[results['Column'] == 'numeric_outliers']
            self.assertTrue(len(numeric_flags) > 0)
            self.assertTrue(any(numeric_flags['Value'] == 100))
            
            # Verify text rare values were caught
            text_flags = results[results['Column'] == 'text_rare']
            self.assertTrue(len(text_flags) > 0)
            self.assertTrue(all(v in ['B', 'C', 'D', 'E', 'F', 'G', 'H'] 
                              for v in text_flags['Value']))
            
            # Verify date format issues were caught
            date_flags = results[results['Column'] == 'date_invalid']
            self.assertTrue(len(date_flags) > 0)
            self.assertTrue(all('Date Format Mismatch' in str(m) 
                              for m in date_flags['Method']))
            
            # Cleanup
            output_path.unlink()
            
    def test_full_pipeline_std(self):
        """Test the complete dictionary checker pipeline using STD method"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            output_path = Path(tmp.name)
            
            # Run the checker with STD method
            run_dictionary_checker(
                df=self.df,
                dict_df=self.dict_df,
                domain='TestDomain',
                output_path=output_path,
                outlier_method=OutlierMethod.STD
            )
            
            # Read and validate results
            results = pd.read_csv(output_path)
            
            # Verify numeric outliers were caught with STD method
            numeric_flags = results[results['Column'] == 'numeric_outliers']
            self.assertTrue(len(numeric_flags) > 0)
            self.assertTrue(any(numeric_flags['Value'] == 100))
            self.assertTrue(all('STD Outlier' in str(m) 
                              for m in numeric_flags['Method']))
            
            # Cleanup
            output_path.unlink()
            
    def test_error_handling(self):
        """Test error handling in the full pipeline"""
        # Test with invalid dictionary
        invalid_dict = pd.DataFrame({
            'Main Variable': ['invalid_col'],
            'Type': ['invalid_type'],
            'Value': [''],
            'Description': ['Invalid column test']
        })
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            output_path = Path(tmp.name)
            
            # Run checker with invalid dictionary
            run_dictionary_checker(
                df=self.df,
                dict_df=invalid_dict,
                domain='TestDomain',
                output_path=output_path,
                outlier_method=OutlierMethod.IQR
            )
            
            # Verify results were still created
            self.assertTrue(output_path.exists())
            results = pd.read_csv(output_path)
            self.assertTrue(results.empty)  # No valid results expected
            
            # Cleanup
            output_path.unlink()

if __name__ == '__main__':
    unittest.main()