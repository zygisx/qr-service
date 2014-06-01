# coding=utf-8
from datetime import datetime
import requests


DATE_FORMAT_IN = '%Y-%m-%d'
DATE_FORMAT_OUT = '%Y%m%d'


class Invoice(object):

    def __init__(self, date, purchaseDate, invoiceSerie, invoiceNumber, provider, receiver, items):
        self.invoiceSerie = invoiceSerie
        self.invoiceNumber = invoiceNumber
        self.provider = provider
        self.receiver = receiver

        self.__date = datetime.strptime(date, DATE_FORMAT_IN)
        self.__purchaseDate = datetime.strptime(purchaseDate, DATE_FORMAT_IN)

        self.items = []
        for item in items:
            self.items.append(Item(
                id=item['id'],
                units=item['units'], 
                unitPrice=item['unitPrice'],
                taxableValue=item['taxableValue'],
                vat=item['vat'],
                vatAmount=item['vatAmount']
            ))


    @property
    def date(self):
        return self.__date.strftime(DATE_FORMAT_OUT)

    @property
    def purchaseDate(self):
        return self.__purchaseDate.strftime(DATE_FORMAT_OUT)

class Item(object):

    def __init__(self, id, units, unitPrice, taxableValue, vat, vatAmount):
        self.id = id
        self.units = units
        self.unitPrice = unitPrice
        self.taxableValue = taxableValue
        self.vat = vat
        self.vatAmount = vatAmount


class EncodeService(object):

    def __init__(self):
        pass

    def encode(self, request_dict):
        invoice = Invoice(
            date=request_dict['date'],
            purchaseDate=request_dict['purchaseDate'],
            invoiceSerie=request_dict['invoiceSerie'],
            invoiceNumber=request_dict['invoiceNumber'],
            provider=request_dict['providerId'],
            receiver=request_dict['receiverId'],
            items=request_dict['items']
        )

        result = str(invoice.date) + \
            str(invoice.purchaseDate) + \
            self.string_to_numbers(invoice.invoiceSerie) + \
            self.fill_leading_zeros(invoice.invoiceNumber, 30, "sąskaitos numeris") + \
            self.fill_leading_zeros(invoice.provider, 13, "pardavėjas") + \
            self.fill_leading_zeros(invoice.receiver, 13, "pirkėjas") + \
            self.fill_leading_zeros(len(invoice.items), 3, "prekių skaičius")

        for item in invoice.items:
            result += self.fill_leading_zeros(item.id, 13, "prekės id") + \
                self.fill_leading_zeros(item.units, 7, "prekės vienetu skaičius") + \
                self.fill_leading_zeros(item.unitPrice, 12, "prekės vieneto kaina") + \
                self.fill_leading_zeros(item.taxableValue, 12, "prekės apmokestinama vertė") + \
                self.fill_leading_zeros(item.vat, 2, "pvm tarifas") + \
                self.fill_leading_zeros(item.vatAmount, 12, "pvm suma")

        if not result.isdigit():
            raise Exception("Non number value entered.")

        return result

    def string_to_numbers(self, string):
        numbers = ""
        for symbol in string:
            numbers += "%02d" % self.symbol_to_number(symbol)
            # or could be str('a15f').zfill(5)
        return numbers

    def symbol_to_number(self, symbol):
        return ord(symbol) - 32

    def fill_leading_zeros(self, string, length, field_value=""):
        if len(str(string)) > length: raise Exception("Per ilga reikšmė lauke " + field_value)
        return str(string).zfill(length)


class DecodeService(object):

    def __init__(self):
        pass

    def decode_image(self, file):
        url = 'http://api.qrserver.com/v1/read-qr-code/'
        files = {'file': file.stream}
        r = requests.post(url, files=files)
        result = r.json()
        symbol = result[0]["symbol"]
        if not symbol[0]["error"]:
            data = symbol[0]["data"]
            print data
            return self.decode(data)
        else:
            raise Exception("Negaliu nuskaityti QR kodo")

    def decode(self, data):
        if not data.isdigit():
            raise Exception("Netinkamas sąskaitos faktūros formatas")

        data = str(data)

        result = {}
        result["date"] = self.decode_date(data[0:8])
        result["purchaseDate"] = self.decode_date(data[8:16])
        result["invoiceSerie"] = self.numbers_to_string(data[16:22])
        result["invoiceNumber"] = self.remove_leading_zeros(data[22:52])
        result["providerId"] = self.remove_leading_zeros(data[52:65])
        result["receiverId"] = self.remove_leading_zeros(data[65:78])

        items_count = int(data[78:81])
        items = []
        for i in range(items_count):
            pos = i*58
            item = {}
            item["id"] = self.remove_leading_zeros(data[pos+81:pos+94])
            item["units"] = self.remove_leading_zeros(data[pos+94:pos+101])
            item["unitPrice"] = self.remove_leading_zeros(data[pos+101:pos+113])
            item["taxableValue"] = self.remove_leading_zeros(data[pos+113:pos+125])
            item["vat"] = self.remove_leading_zeros(data[pos+125:pos+127])
            item["vatAmount"] = self.remove_leading_zeros(data[pos+127:pos+138])
            items.append(item)

        result["items"] = items

        return result

    def decode_date(self, date):
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        return "%s-%s-%s" % (year, month, day)

    def numbers_to_string(self, numbers):
        string = ""
        for i in range(0, len(numbers), 2):
            number = int("%s%s" % (numbers[i], numbers[i+1]))
            string += self.number_to_string(number)

        return string

    def number_to_string(self, number):
        return chr(int(number) + 32)

    def remove_leading_zeros(self, string):
        return string.lstrip("0")



