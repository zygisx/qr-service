# -*- coding: utf-8 -*-
__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from qr_service import app
from qr_service.services import EncodeService, DecodeService
from flask.globals import request
from flask.json import jsonify
from flask.helpers import send_file
import qrcode
from qrcode.image.pure import PymagingImage
from StringIO import StringIO
import base64
import requests


encode_service = EncodeService()
decode_service = DecodeService()
DEFAULT_ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_M


def get_error_correction_type(req):
    code = req.get("errorCorrection", DEFAULT_ERROR_CORRECTION)
    if code == 'L': return qrcode.constants.ERROR_CORRECT_L
    elif code == 'M': return qrcode.constants.ERROR_CORRECT_M
    elif code == 'Q': return qrcode.constants.ERROR_CORRECT_Q
    elif code == 'H': return qrcode.constants.ERROR_CORRECT_H
    else: return DEFAULT_ERROR_CORRECTION

@app.route('/api/encode', methods=["POST"])
def encode():
    # just a sample encoding
    req = request.json

    print "Request:", req

    # data = req["data"]
    data = encode_service.encode(req)
    error_correction_code = get_error_correction_type(req)

    img = qrcode.make(data, error_correction=error_correction_code,
                      image_factory=PymagingImage)

    output = StringIO()
    img.save(output)

    encoded_string = base64.b64encode(output.getvalue())
    print encoded_string

    return jsonify(image=encoded_string, msg="")

@app.route('/api/decodeImage', methods=["POST"])
def decodeImage():
    file = request.files.values()[0]

    result = decode_service.decode_image(file)
    return jsonify(
        result
    )


@app.route('/api/decode', methods=["POST"])
def decode():
    req = request.json
    result = decode_service.decode(req["data"])
    return jsonify(
        result
    )


#####
# Code for pdf report generation
#

from fpdf import FPDF

from flask import render_template, make_response, url_for
import os

abolute = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/fonts/dejavu-fonts-ttf-2.34/ttf/DejaVuSans.ttf')

def create_pdf():
    stringIo = StringIO()

    pdf = FPDF()
    pdf.add_page()

    print abolute

    pdf.add_font('DejaVu', '', abolute, uni=True)
    pdf.set_font('DejaVu', '', 14)

    # pdf.set_font('Arial', 'B', 16)
    print 'SĄSKAITA FAKTŪRA'
    pdf.cell(40, 10, 'SĄSKAITA FAKTŪRA')
    res = pdf.output(dest='S')
    stringIo.write(res)

    return stringIo


@app.route('/api/pdf')
def pdf_report(**kwargs):

    pdf = create_pdf()

    response = make_response(pdf.getvalue())
    response.headers['Content-Disposition'] = "attachment; filename='SF.pdf"
    response.mimetype = 'application/pdf'

    return response