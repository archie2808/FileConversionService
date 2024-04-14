import unittest
from flask import Flask, jsonify, request
from io import BytesIO
from unittest.mock import patch
from src.app_factory import create_app
from src.converter_factory import ConverterFactory
from src.utility import scan_file_with_clamav

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)  # Configure your Flask app for testing
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_convert_file_same_formats(self):
        data = {'target_format': 'txt', 'file': (BytesIO(b"dummy data"), 'test.txt')}
        response = self.client.post('/convert', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Source and target formats cannot be the same', response.get_json()['error'])

    @patch('src.converter_factory.ConverterFactory.get_converter')
    def test_convert_file_successful(self, mock_get_converter):
        mock_converter = mock_get_converter.return_value
        mock_converter.convert.return_value = BytesIO(b"PDF data")
        data = {'target_format': 'pdf', 'file': (BytesIO(b"dummy data"), 'test.docx')}
        response = self.client.post('/convert', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/pdf', response.content_type)

    def test_validate_file_no_file_part(self):
        response = self.client.post('/validate_file')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file part', response.get_json()['error'])

    def test_validate_file_no_selected_file(self):
        data = {'file': (BytesIO(b''), '')}
        response = self.client.post('/validate_file', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('No selected file', response.get_json()['error'])

    @patch('src.utility.scan_file_with_clamav')
    def test_validate_file_malicious(self, mock_scan):
        mock_scan.return_value = "Virus found"
        data = {'file': (BytesIO(b'dummy data'), 'test.exe')}
        response = self.client.post('/validate_file', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Malicious file detected', response.get_json()['error'])

    def tearDown(self):
        # clean up / reset resources here if necessary
        pass

if __name__ == '__main__':
    unittest.main()

