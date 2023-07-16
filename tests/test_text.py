import unittest, os
from qrcode_library import *


class TestText(unittest.TestCase):

    def test_text___no_errors(self):

        file = os.path.join(os.path.dirname(__file__), 'test_output', 'text.png')

        if os.path.isfile(file):
            os.remove(file)
        
        qr = QRCodeText('Test successfull')
        image = qr.create_image()
        image.save(file)

        self.assertEquals(os.path.isfile(file), True)

    def test_text___value_error(self):

        with self.assertRaises(ValueError):
            QRCodeText(10)