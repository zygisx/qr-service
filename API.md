# QR serviso API aprašymas

QR servisas naudoja JSON tipą komunikacijai tarp kliento ir serverio.
Visos operacijos atliekamos naudojant `HTTP POST` metodą.


## Sąskaitos faktūros kodavimas

Norint gauti užkoduotą sąskaitą faktūra QR kodo pavidalu kviečiamas:

>  HTTP POST /api/encode

Kvietimo metu perduodami sąskaitos faktūros duomenys JSON tipo.

Perduodami duomenys:

 - `date` - sąsakitos faktūros pasirašymo data formatu YYYY-MM-DD
 - `purchaseDate` - sandorio įvykdymo data formatu YYYY-MM-DD
 - `invoiceSerie` - sąskaitos faktūros serijos numeris (3 simboliai)
 - `invoiceNumber` - sąskaitos faktūros unikalus numeris serijai (iki 6 skaitmenų)
 - `providerId` - pardavėjo unikalus identifikatorius (iki 13 skaitmenų)
 - `receiverId` - pirkėjo unikalus identifikatorius (iki 13 skaitmenų)
 - `items` - prekių sąrašas :
    - `id` - prekės unikalus identifikatorius (iki 13 skaitmenų)
    - `units` - prekės vienetų skaičius (iki 6 skaitmenų)
    - `unitPrice` - prekės vieneto kaina centais (iki 8 skaitmenų)
    - `taxableValue` - prekės apmokestinama verte centais (iki 8 skaitmenų)
    - `vat` - pridėtinės vertės tarifas procentais (iki 2 skaitmenų)
    - `vatAmount` - PVM suma centais (iki 8 skaitmenų)

Pavyzdžiui:
```json
{
  "date": "2014-05-26",
  "purchaseDate": "2014-05-26",
  "invoiceSerie": "ABC",
  "invoiceNumber": 123456,
  "receiverId": 50322,
  "providerId": 5790343226,
  "items": [
    {
      "vatAmount": 123,
      "units": 3,
      "taxableValue": 23,
      "unitPrice": 123,
      "id": 12345678,
      "vat": 21
    },
    ...
  ]
}
```

Grąžinami duomenys:

QR servisas gražina json tipo objektą kuriame yra:
  - `image` - base64 formatu užkoduotas PNG tipo QR kodo atvaizdas
  - `msg` - pranešimas iš serverio (jei įvyko klaida).

Pavyzdžiui:
```json
{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaCAIAAAC.....",
  "msg": ""
}
```


## Sąskaitos faktūros kodavimas

Sąskaitą faktūra galima iškoduoti dviejais būdais. Arba QR servisui perduoti QR kodo atvaizdo paveikslėlį PNG formatu arba QR servisui perduoti iškoduotą skaičių eilutę.
Antrasis būdas naudojamas jei QR kodo nuskaitymui naudojama specialiai tam skirta techninė įranga.

#### QR kodo atvaizdo su sąskaitų faktūrų duomenimis iškodavimas

Jei norime iškoduoti QR kodo atvaizdą kviečiame:

>  HTTP POST /api/decodeImage

metodą, perduodami paveikslėlį PNG formatu.

#### Sąskaitų faktūrų duomenų iškodavimas

Jei norime iškoduoti sąskaitų faktūrų duomenis, ir paveiksliukas buvo atkoduotas naudojant QR kodų skaitytuvą kviečiame:

>  HTTP POST /api/decode

Kviečiasdami perduodame JSON tipo objektą iš vieno lauko:
  - `data` - skaičių eilutė, gauta iškodavus QR kodo atvaizdą.

Pavyzdžiui:
```json
{
  "data": "201405262014042665666700011100000000002220000000000333002..."
}
```

Nesvarbu ar iškoduojame paveiksliuką ar skaičių seką abiem atvejais servisas grąžina JSON tipo objektą, kuriame yra
atkoduotos sąskaitos faktūros informacija:
   - `date` - sąsakitos faktūros pasirašymo data formatu YYYY-MM-DD
   - `purchaseDate` - sandorio įvykdymo data formatu YYYY-MM-DD
   - `invoiceSerie` - sąskaitos faktūros serijos numeris (3 simboliai)
   - `invoiceNumber` - sąskaitos faktūros unikalus numeris serijai (iki 6 skaitmenų)
   - `providerId` - pardavėjo unikalus identifikatorius (iki 13 skaitmenų)
   - `receiverId` - pirkėjo unikalus identifikatorius (iki 13 skaitmenų)
   - `items` - prekių sąrašas :
     - `id` - prekės unikalus identifikatorius (iki 13 skaitmenų)
     - `units` - prekės vienetų skaičius (iki 6 skaitmenų)
     - `unitPrice` - prekės vieneto kaina centais (iki 8 skaitmenų)
     - `taxableValue` - prekės apmokestinama verte centais (iki 8 skaitmenų)
     - `vat` - pridėtinės vertės tarifas procentais (iki 2 skaitmenų)
     - `vatAmount` - PVM suma centais (iki 8 skaitmenų)

Pavyzdžiui:
```json
{
  "date": "2014-05-26",
  "purchaseDate": "2014-04-26",
  "invoiceSerie": "abc",
  "invoiceNumber": "111",
  "providerId": "222",
  "receiverId": "333",
  "items": [
    {
      "id": "444",
      "taxableValue": "777",
      "unitPrice": "666",
      "units": "555",
      "vat": "88",
      "vatAmount": "999"
    },
    {
      "id": "555",
      "taxableValue": "888",
      "unitPrice": "777",
      "units": "666",
      "vat": "99",
      "vatAmount": "1000"
    }
  ]
}
```
