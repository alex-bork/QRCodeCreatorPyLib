import unittest, os
from qrcode_library import *


class TestSMS(unittest.TestCase):

    def test_sms___no_errors(self):

        file = os.path.join(os.path.dirname(__file__), 'test_output', 'sms.png')

        if os.path.isfile(file):
            os.remove(file)
        
        qr = QRCodeSMS('+49 16012345678', 'Test Successfull')
        image = qr.create_image()
        image.save(file)

        self.assertEquals(os.path.isfile(file), True)

    def test_sms___string_value_error(self):

        with self.assertRaises(ValueError):
            QRCodeSMS(10, 'Test Failed')

        with self.assertRaises(ValueError):
            QRCodeSMS('+49 16012345678', 10)

    def test_sms___phone_validation_error(self):

        with self.assertRaises(ValueError):
            QRCodePhone('016012A345678')
        with self.assertRaises(ValueError):
            QRCodePhone('+4901601234#5678')

    def test_sms___phone_validation_success(self):

        qr = QRCodePhone('+49 16012345678')
        self.assertIsInstance(qr, QRCodePhone)
        qr = QRCodePhone('016012345678')
        self.assertIsInstance(qr, QRCodePhone)
        qr = QRCodePhone('+49531 28877275')
        self.assertIsInstance(qr, QRCodePhone)
        qr = QRCodePhone('0511 394458595-33')
        self.assertIsInstance(qr, QRCodePhone)

        