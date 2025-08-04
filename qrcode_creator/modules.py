import base64
from dataclasses import dataclass
from datetime import date
import math
from typing import Literal, Optional, Union
import PIL
import qrcode
from qrcode import constants as qrconst
from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer,
    RoundedModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)
from qrcode.image.styledpil import StyledPilImage
from enum import Enum
import os
from PIL import Image
import base64
import validators
import re


class ValueChecks:
    @staticmethod
    def phone_number_is_valid(phone_number: str) -> bool:
        pattern = re.compile(r'^[+|\d][\d| |-]+$')
        return pattern.match(phone_number)
    
    @staticmethod
    def email_is_valid(email: str) -> bool:
        pattern = re.compile(r'^([^@]+)@([^@]+)\.([a-zA-Z]{2,3})$')
        return pattern.match(email)
    
    @staticmethod
    def ssid_is_valid(ssid: str) -> bool:
        pattern = re.compile(r'^[^\?\"\$\[\]\+\\]+$')
        return pattern.match(ssid)
    
    @staticmethod
    def geo_coordinate_is_valid(coordinate: str) -> bool:
        pattern = re.compile(r'^\d\d.\d\d\d\d\d\d$')
        return pattern.match(coordinate)


class ContentNotAccepted(Exception):
    pass


class QRCodeCreatorTypes(Enum):
    
    Text = 1
    Wifi = 2


class WifiEncryption(Enum):
    
    WEP = 1
    WPA = 2


class QRCodeBase:

    _MAX_ICON_SIZE_FACTOR = 0.10
    _qrcode: any = None
    _icon_path: str = None

    def __init__(self):
        self._qrcode = qrcode.QRCode(error_correction=qrconst.ERROR_CORRECT_H)

    def _add_data(self, 
                  data: any) -> None:
        self._qrcode.add_data(data)
        self._qrcode.make(fit=True)

    def _init_default_icon(self) -> None:
        icon_name = type(self).__name__.split('QRCode')[1] + '.png'
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', icon_name)
        if os.path.isfile(icon_path):
            self._icon_path = icon_path

    def _get_border_size(self, qr_height: int) -> int:
        return self._qrcode.border * self._qrcode.box_size * qr_height * 4

    def _set_icon(self, 
                  qr_image: any) -> None:
        icon = Image.open(self._icon_path)
        icon_width, icon_height = icon.size         
        qr_width, qr_height = qr_image.size
        qr_total_size = qr_width * qr_height - self._get_border_size(qr_height)

        icon_target_size = self._MAX_ICON_SIZE_FACTOR * qr_total_size
        icon_width_factor = icon_width // icon_height

        new_icon_width = math.sqrt(icon_target_size) * icon_width_factor
        new_icon_hight = icon_target_size / new_icon_width

        icon = icon.resize((int(new_icon_width), int(new_icon_hight)), PIL.Image.LANCZOS)

        pos = (int((qr_width - new_icon_width) // 2), int((qr_height - new_icon_hight) // 2))

        qr_image.paste(icon, pos)

    def _get_module_drawer(self, qr_style):

        if qr_style == "squared":
            return SquareModuleDrawer()
        elif qr_style == "gapped":
            return GappedSquareModuleDrawer()
        elif qr_style == "circle":
            return CircleModuleDrawer()
        elif qr_style == "rounded":
            return RoundedModuleDrawer()
        elif qr_style == "verticalbars":
            return VerticalBarsDrawer()
        elif qr_style == "horizontalbars":
            return HorizontalBarsDrawer()
        else:
            raise ValueError(f"QR stype {qr_style} not supported.")

    def create_image(self, 
                     fill_color: tuple = (0, 0, 0), 
                     back_color: tuple = (255, 255, 255), 
                     border: int = 4, 
                     qr_style: Optional[Literal["squared", "gapped", "circle", "rounded", "verticalbars", "horizontalbars"]] = "squared",
                     box_size: Union[int, None] = None,
                     icon_path: Union[str, None] = None,
                     use_default_icon: bool = False):

        if border < 4:
            raise ValueError('border must not have value lower than 4.')
        self._qrcode.border = border

        if box_size:
            self._qrcode.box_size = box_size

        module_drawer = self._get_module_drawer(qr_style)

        qr_image = self._qrcode.make_image(
            fill_color=fill_color, 
            back_color=back_color, 
            module_drawer=module_drawer,
            image_factory=StyledPilImage
        )

        if use_default_icon:
            self._init_default_icon()
        if icon_path and os.path.isfile(icon_path):
            self._icon_path = icon_path
        if self._icon_path:
            self._set_icon(qr_image)

        return qr_image


class QRCodeText(QRCodeBase):

    def __init__(self, 
                 text: str):
        if not isinstance(text, str):
            raise ValueError('Parameter text is not a string.')
        super().__init__()
        self._add_data(text)


class QRCodeLink(QRCodeBase):

    def __init__(self, 
                 link: str):
        if not isinstance(link, str):
            raise ValueError('Parameter link is not a string.')
        if not validators.url(link):
            raise ValueError(f'{link} is not a valid link.')
        super().__init__()
        self._add_data(link)


@dataclass(init=True)
class QRCodeGeoLocationData:
    '''
    ATTRIBUTES

    - [ latitude ] string format: DD.DDDDDD
    - [ longitude ] string format: DD.DDDDDD
    '''
    latitude: str
    longitude: str


class QRCodeGeoLocation(QRCodeBase, ValueChecks):

    def __init__(self, 
                 geo_data: QRCodeGeoLocationData):
        if not isinstance(geo_data, QRCodeGeoLocationData):
            raise ValueError('Paramter geo_data has wrong type.')
        if not isinstance(geo_data.latitude, str) or not isinstance(geo_data.longitude, str):
            raise ValueError('Coordinates must be string type.')
        if not self.geo_coordinate_is_valid(geo_data.longitude):
            raise ValueError('Value(s) of geo_data are not valid. Use pattern DD.DDDDDD.')
        if not self.geo_coordinate_is_valid(geo_data.longitude):
            raise ValueError('Value(s) of geo_data are not valid. Use pattern DD.DDDDDD.')
        super().__init__()
        self._add_data(f'GEO:{geo_data.latitude},{geo_data.longitude}')


class QRCodePhone(QRCodeBase, ValueChecks):

    def __init__(self, 
                 phone_number: str):
        if not isinstance(phone_number, str):
            raise ValueError('Parameter phone_number is not a string.')
        if not self.phone_number_is_valid(phone_number):
            raise ValueError('Parameter phone_number is not valid.')
        super().__init__()
        self._add_data(f'TEL:{phone_number}')


class QRCodeSMS(QRCodeBase, ValueChecks):

    def __init__(self, 
                 phone_number: str,
                 message: str = ''):
        super().__init__()
        if not isinstance(phone_number, str) or not isinstance(message, str):
            raise ValueError('Either of the parameter is not a string')
        if not self.phone_number_is_valid(phone_number):
            raise ValueError('Parameter phone_number is not valid.')
        phone_number = phone_number.replace(' ', '')
        self._add_data(f'SMSTO:{phone_number}:{message}')


class QRCodeEmail(QRCodeBase, ValueChecks):

    def __init__(self, 
                 email: str,
                 subject: str,
                 text: str = ''):
        if not isinstance(email, str) or not isinstance(subject, str) or not isinstance(text, str):
            raise ValueError('One of the parameters is not a string.')
        if not self.email_is_valid(email):
            raise ValueError('Email address is not valid')
        super().__init__()
        self._add_data(f'MAILTO:{email}?SUBJECT={subject}&BODY={text}')


class QRCodeWifi(QRCodeBase, ValueChecks):

    def __init__(self, 
                 ssid: str, 
                 encrypt: WifiEncryption, 
                 password: str, 
                 hidden: Union[bool, None] = None ):
        if not isinstance(ssid, str) or not isinstance(password, str) or (not isinstance(password, str)):
            raise ValueError('One or more parameters with wrong type.')
        if not isinstance(encrypt, WifiEncryption) or not encrypt.name in WifiEncryption.__members__:
            raise ValueError('Type or value of parameter encrypt is not valid.')
        if not self.ssid_is_valid(ssid):
            raise ValueError('SSID is not valid.')
        if not hidden == None and not isinstance(hidden, bool):
            raise ValueError('Parameter hidden has wrong value or type.')
        super().__init__()
        wifi_string = f'WIFI:S:{ssid};T:{encrypt.name};P:{password}'
        if hidden:
            wifi_string += ';H:true'
        wifi_string += ';;'
        self._add_data(wifi_string)


# class QRCodeEventClass(Enum):
#     PRIVATE = 1
#     PUBLIC = 2


# class QRCodeEventMethod(Enum):
#     PUBLISH = 1
#     REQUEST = 2


# class QRCodeEventRecuranceFrequency(Enum):
#     DAILY = 1
#     WEEKLY = 2
#     MONTHLY = 3
#     YEARLY = 4


# class QRCodeEventRecuranceDay(Enum):
#     MO = 1
#     TU = 2
#     WE = 3
#     TH = 4
#     FR = 5
#     ST = 6
#     SU = 7


# @dataclass
# class QRCodeEventRecurance:
#     '''
#     ATTRIBUTES

#         - [ frequency ]       dayly, weekly, monthly, yearly
#         - [ until format ]   <yyyymmdd>T<hhmmss>(Z)
#         - [ interval ]       number for interval
#         - [ count ]          occurences
#         - [ byday ]          1 - 31, on which day(s), example: byday =
#         - [ bymonth ]        1 - 12
#     '''
#     frequency: QRCodeEventRecuranceFrequency
#     until: str
#     interval: int
#     count: int
#     bymonth: int


# class QRCodeEvent(QRCodeBase):

#     def __init__(self,
#                  name: str,
#                  description: str,
#                  location: str,
#                  start_date: str,
#                  start_time: str,
#                  end_date: str,
#                  end_time: str,
#                  url: Union[str, None] = '',
#                  geo_location: Union[QRCodeGeoLocationData, None] = '',
#                  event_class: QRCodeEventClass = QRCodeEventClass.PUBLIC,
#                  method: QRCodeEventMethod = QRCodeEventMethod.PUBLISH,
#                  ):
#         '''
#         CLASS:      is the event private or public?
#         METHOD:     should this event be a request or be published into the calender directly?
#         DTSTAMP:    system date, when the event has been created, in order to check if event on the client system has to be updated.
#         '''
#         super().__init__()

#         uid = base64.b64encode(f'{name} {location} {start_date} {start_time}'.encode("utf-8"))
#         today = date.today()
#         dtstamp = f'{today.year}{today.month}{today.day}'
#         calender_string = ('BEGIN:VCALENDAR' +
#                             '\nBEGIN:VEVENT' +

#                             f'\nUID:{uid}' +
#                             f'\nCLASS:{event_class.name}' +
#                             f'\nMETHOD:{method.name}' +
#                             f'\nSUMMARY:{name}' +
#                             f'\nDESCRIPTION:{description}'
#                             f'\nLOCATION:{location}'
#                             f'\nGEO:{geo_location.latitude};{geo_location.longitude}'
#                             f'\nURL:{url}' +
#                             f'\nDTSTART:{start_date}T{start_time}' +
#                             f'\nDTEND:{end_date}T{end_time}' +
#                             f'\nDTSTAMP:{dtstamp}'

#                             '\nEND:VEVENT' +
#                             '\nEND:VCALENDAR')
#         self._add_data(calender_string)


@dataclass(init=True)
class QRCodeVCardUrl:
    address: str


@dataclass(init=True)
class QRCodeVCardEmail:
    address: str


@dataclass(init=True)
class QRCodeVCardAddress:
    street: str
    street_number: str
    zip_code: str
    city: str
    state: str
    country: str


@dataclass(init=True)
class QRCodeVCardPhone:
    '''ATTRIBUTES \n
        - [ type ]    could be for example "Private" or "Public", or self defined one
        - [ number ]  phone number
    '''
    number: str


class QRCodeVCard(QRCodeBase):

    def __init__(self, 
                 firstname: str = '', 
                 lastname: str = '', 
                 prefix: str = '',
                 suffix: str = '', 
                 organisation: str = '', 
                 jobtitle: str = '',
                 phones: Union[list[QRCodeVCardPhone], None] = None,
                 emails: Union[list[QRCodeVCardEmail], None] = None,
                 urls: Union[list[QRCodeVCardUrl], None] = None,
                 addresses: Union[list[QRCodeVCardAddress], None] = None):
        if not firstname and not lastname:
            raise ValueError('Surname or Lastname must be supplied.')
        if not isinstance(firstname, str) or not isinstance(lastname, str) or not isinstance(prefix, str) or \
            not isinstance(suffix, str) or not isinstance(organisation, str) or not isinstance(jobtitle, str):
            raise ValueError('One of the supplied parameters does not have type string.')
        if phones:
            if not isinstance(phones, list) or len([phone for phone in phones if not isinstance(phone, QRCodeVCardPhone)]) != 0:
                raise ValueError('Phones has wrong type. Use type: list[QRCodeVCardPhone]')
        if emails:
            if not isinstance(emails, list) or len([email for email in emails if not isinstance(email, QRCodeVCardEmail)]) != 0:
                raise ValueError('Emails has wrong type. Use type: list[QRCodeVCardEmail]')
        if urls:
            if not isinstance(urls, list) or len([url for url in urls if not isinstance(url, QRCodeVCardUrl)]) != 0:
                raise ValueError('Urls has wrong type. Use type: list[QRCodeVCardUrl]')
        if addresses:
            if not isinstance(addresses, list) or len([address for address in addresses if not isinstance(address, QRCodeVCardAddress)]) != 0:
                raise ValueError('Addresses has wrong type. Use type: list[QRCodeVCardAddress]')           
        super().__init__()
        vcard_string = (
                        'BEGIN:VCARD\nVERSION:4.0\n' + 
                        f'\nN:{lastname};{firstname};{prefix};{suffix};' +
                        f'\nFN:{firstname} {lastname}' + 
                        f'\nORG:{organisation}' + 
                        f'\nTITLE:{jobtitle}'
                        )

        if urls:
            for url in urls:
                vcard_string += f'\nURL:{url.address}'

        if emails:
            for email in emails:
                vcard_string += f'\nEMAIL:{email.address}'

        if addresses:
            for address in addresses:
                vcard_string += f'\nADR:;;{address.street} {address.street_number};{address.city};{address.state};{address.zip_code};{address.country}'

        if phones:
            for phone in phones:
                vcard_string += f'\nTEL:{phone.number}'

        vcard_string += '\nEND:VCARD'

        self._add_data(vcard_string)


if __name__ == '__main__':

    # #TEXT

    qr = QRCodeText("Exsample Test is OK.")
    img = qr.create_image(qr_style="verticalbars")
    img.save("QRTypeText.png")


# #LINK

# qr = QRCodeLink(link=r'<a href="tel:123-456-7890">ddd</a>')
# img = qr.create_image(qr_style="circle")
# img.save("QRTypeLink.png")


# #GEOLOCATION

#     qr = QRCodeGeoLocation(QRCodeGeoLocationData(latitude='52.251723474830776',
#                                                  longitude='10.467977442471788'))
#     img = qr.create_image()
#     img.save("QRTypeGeoLocation.png")


# #PHONE

#     qr = QRCodePhone('+49 16098085161')
#     img = qr.create_image()
#     img.save("QRTypePhone.png")


# #SMS

#     qr = QRCodeSMS(phone_number='+49 16098085161', message= 'Test OK')
#     img = qr.create_image()
#     img.save("QRTypeSMS.png")


# #VCARD

#     qr = QRCodeVcard(firstname='Alex',
#                      lastname='Bork',
#                      phones=[QRCodeVcardPhone(type='Mobile', number='+49 16098085161')],
#                      urls=[QRCodeVcardUrl(type='Privat', address='http://home.de')],
#                      emails=[QRCodeVcardEmail(type='Privat', address='alex.bork@outlook.com')],
#                      addresses=[QRCodeVcardAddress(type='Privat', state='Niedersachsen', street='Mainweg',street_number='1', zip_code="38120", city='Braunschweig', country="Germany")]
#                     )
#     img = qr.create_image()
#     img.save("QRTypeVcard.png")


# #WIFI

#     qr = QRCodeWifi(ssid='FRITZ!Box 7530 AS', encrypt=WifiEncryption.WPA, password='68613528323499691573')
#     img = qr.create_image()
#     img.save("QRTypeWifi.png")


# #EMAIL

#     qr = QRCodeEmail(email='alex.bork@outlook.com', subject='Test QR-Code')
#     img = qr.create_image()
#     img.save("QRTypeEMail.png")


# #CALENDEREVENT

#     qr = QRCodeEvent(name='EventName11',
#                              description='EventDescription',
#                              location='EventLocation',
#                              geo_location=QRCodeGeoLocationData(latitude='52.251723474830776',
#                                                                 longitude='10.467977442471788'),
#                              start_date='20230422',
#                              start_time='110000',
#                              end_date='20230422',
#                              end_time='133000')
#     img = qr.create_image()
#     img.save("QRTypeCalenderEvent.png")
