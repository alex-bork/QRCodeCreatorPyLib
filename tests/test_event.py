# import unittest, os
# from qrcode_creator import *


# class TestEvent(unittest.TestCase):

#     def test_event___no_errors(self):

#         file = os.path.join(os.path.dirname(__file__), 'test_output', 'event.png')

#         if os.path.isfile(file):
#             os.remove(file)
        
#         qr = QRCodeEvent('Test Event', 'Test Description', 'Braunschweig', )
#         image = qr.create_image()
#         image.save(file)

#         self.assertTrue(os.path.isfile(file))