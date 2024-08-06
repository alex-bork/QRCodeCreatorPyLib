import unittest, os
from qrcode_creator import *


class TestVCard(unittest.TestCase):

    def test_vcard__no_errors(self):

        file = os.path.join(os.path.dirname(__file__), 'test_output', 'vcard.png')

        if os.path.isfile(file):
            os.remove(file)
        
        qr = QRCodeVCard(firstname='Max', 
                        lastname='Mustermann', 
                        phones=[QRCodeVCardPhone(number='+49 16012345678')],
                        urls=[QRCodeVCardUrl(address='http://home.de')],
                        emails=[QRCodeVCardEmail(address='max.mustermann@outlook.com')],
                        addresses=[QRCodeVCardAddress(state='Niedersachsen', street='Berliner Allee',street_number='1', zip_code="38100", city='Braunschweig', country="Germany")]
                        )

        image = qr.create_image()
        image.save(file)

        self.assertTrue(os.path.isfile(file))


    def test_vcard___value_errors(self):

        with self.assertRaises(ValueError):
            QRCodeVCard(10, 'Mustermann')

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 10)

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 10)

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 10)

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 10)

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 10)

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 'Software Engineer', 
                [10])

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 'Software Engineer', 
                [QRCodeVCardPhone('+49 16012345678')], [10])

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 'Software Engineer', 
                [QRCodeVCardEmail('max.mustermann@outlook.com')], [10])

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 'Software Engineer', 
                [QRCodeVCardEmail('max.mustermann@outlook.com')], 
                [QRCodeVCardUrl('https://test.de')], [10])

    def test_vcard___validation_errors(self):

        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 'Software Engineer', 
                [QRCodeVCardPhone('+49 A16012345678')], [10])
            
        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 'Software Engineer', 
                [QRCodeVCardEmail('max.mustermann.outlook.com')], [10])
            
        with self.assertRaises(ValueError):
            QRCodeVCard('Max', 'Mustermann', 'Mr', 'Test', 'Test Org', 'Software Engineer', 
                [QRCodeVCardEmail('max.mustermann@outlook.com')], 
                [QRCodeVCardUrl('https://test-de')], [10])