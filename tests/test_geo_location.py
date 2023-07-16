import unittest, os
from qrcode_library import *


class TestGeoLocation(unittest.TestCase):

    def test_geo___no_errors(self):

        file = os.path.join(os.path.dirname(__file__), 'test_output', 'geo.png')

        if os.path.isfile(file):
            os.remove(file)

        geo_data = QRCodeGeoLocationData('52.514487', '13.350126')
        
        qr = QRCodeGeoLocation(geo_data)
        image = qr.create_image()
        image.save(file)

        self.assertEquals(os.path.isfile(file), True)

    # def test_wifi___string_value_error(self):

    #     with self.assertRaises(ValueError):
    #         QRCodeWifi(10, WifiEncryption.WPA, 'TestPassword123')

    #     with self.assertRaises(ValueError):
    #         QRCodeWifi('Test_SSID', 'EEP', 'TestPassword123')

    #     with self.assertRaises(ValueError):
    #         QRCodeWifi('Test_SSID', WifiEncryption.WPA, 10)

    # def test_wifi___ssid_validation_error(self):

    #     with self.assertRaises(ValueError):
    #         QRCodeEmail('?Test_SSID', WifiEncryption.WPA, 'TestPassword123')

    #     with self.assertRaises(ValueError):
    #         QRCodeEmail('Test_SSI]D', WifiEncryption.WPA, 'TestPassword123')