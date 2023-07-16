import unittest, os
from qrcode_library import *


class TestEmail(unittest.TestCase):

    def test_email___no_errors(self):

        file = os.path.join(os.path.dirname(__file__), 'test_output', 'email.png')

        if os.path.isfile(file):
            os.remove(file)
        
        qr = QRCodeEmail('max.mustermann@outlook.com', 'Test Subject', 'Test Text')
        image = qr.create_image()
        image.save(file)

        self.assertEquals(os.path.isfile(file), True)

    def test_email___string_value_error(self):

        with self.assertRaises(ValueError):
            QRCodeEmail(10, 'Test Subject', 'Test Text')

        with self.assertRaises(ValueError):
            QRCodeEmail('max.mustermann@outlook.com', 10, 'Test Text')

        with self.assertRaises(ValueError):
            QRCodeEmail('max.mustermann@outlook.com', 'Test Subject', 10)

    def test_email___email_validation_error(self):

        with self.assertRaises(ValueError):
            QRCodeEmail('max@mustermann@outlook.com', 'Test Subject', 'Test Text')

        with self.assertRaises(ValueError):
            QRCodeEmail('max.mustermann@outlook', 'Test Subject', 'Test Text')