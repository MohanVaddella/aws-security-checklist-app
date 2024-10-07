import unittest
from app import app, read_data, write_data
import pandas as pd
import os

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        
        self.app = app.test_client()
        self.app.testing = True
        
        
        self.test_file = 'test_security_controls.xlsx'
        self.test_data = {
            'Control ID': ['1', '2', '3'],
            'Control Description': ['Ensure IAM policies are in place', 'Enable CloudTrail logging', 'Use Security Groups'],
            'Security Level': ['High', 'Medium', 'Low']
        }
        df = pd.DataFrame(self.test_data)
        df.to_excel(self.test_file, index=False)

    def tearDown(self):
        
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_homepage(self):
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cloudhub Security Hub', response.data)

    def test_checklist_page(self):
        
        response = self.app.get('/checklist')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AWS Security Checklist', response.data)

    def test_read_data(self):
        
        data = read_data(self.test_file)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 3)
        self.assertEqual(data.iloc[0]['Control Description'], 'Ensure IAM policies are in place')

    def test_write_data(self):
        
        new_data = {'Control ID': ['4'], 'Control Description': ['New Control'], 'Security Level': ['High']}
        write_data(self.test_file, pd.DataFrame(new_data))
        
        data = read_data(self.test_file)
        self.assertEqual(len(data), 4)
        self.assertEqual(data.iloc[3]['Control Description'], 'New Control')

    def test_search_functionality(self):
        
        response = self.app.get('/checklist?search=CloudTrail')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enable CloudTrail logging', response.data)
        self.assertNotIn(b'Ensure IAM policies are in place', response.data)

if __name__ == '__main__':
    unittest.main()
