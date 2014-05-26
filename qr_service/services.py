
from datetime import datetime


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

        self.items
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

        #validate
        result = str(invoice.date) + \
            str(invoice.purchaseDate) + \
            str(invoice.invoiceSerie) + \
            str(invoice.invoiceNumber) + \
            str(invoice.provider) + \
            str(invoice.receiver)

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

