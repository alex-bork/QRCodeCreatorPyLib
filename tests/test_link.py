import unittest, os
from qrcode_library import *


class TestLink(unittest.TestCase):

    def test_link___no_errors(self):

        file = os.path.join(os.path.dirname(__file__), 'test_output', 'link.png')

        if os.path.isfile(file):
            os.remove(file)
        
        qr = QRCodeLink('https://www.google.de')
        image = qr.create_image()
        image.save(file)

        self.assertEquals(os.path.isfile(file), True)

    def test_link___string_value_error(self):

        with self.assertRaises(ValueError):
            QRCodeLink(10)

    def test_link___link_validation_error(self):

        with self.assertRaises(ValueError):
            QRCodeLink('https://google')