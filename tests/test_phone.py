import unittest, os
from qrcode_library import *


class TestPhone(unittest.TestCase):

    def test_phone___no_errors(self):

        file = os.path.join(os.path.dirname(__file__), 'test_output', 'phone.png')

        if os.path.isfile(file):
            os.remove(file)
        
        qr = QRCodePhone('+49 16012345678')
        image = qr.create_image()
        image.save(file)

        self.assertEquals(os.path.isfile(file), True)

    def test_phone___string_value_error(self):

        with self.assertRaises(ValueError):
            QRCodePhone(10)

    def test_phone___phone_validation_error(self):

        with self.assertRaises(ValueError):
            QRCodePhone('A016012345678')
        with self.assertRaises(ValueError):
            QRCodePhone('+4901601234#5678')

    def test_phone___phone_validation_success(self):

        qr = QRCodePhone('+49 16012345678')
        self.assertIsInstance(qr, QRCodePhone)
        qr = QRCodePhone('016012345678')
        self.assertIsInstance(qr, QRCodePhone)
        qr = QRCodePhone('+49531 28877275')
        self.assertIsInstance(qr, QRCodePhone)
        qr = QRCodePhone('0511 394458595-33')
        self.assertIsInstance(qr, QRCodePhone)

        