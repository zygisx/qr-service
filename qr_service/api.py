# -*- coding: utf-8 -*-
__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from qr_service import app
from flask.globals import request
from flask.json import jsonify
from flask.helpers import send_file
import qrcode
from qrcode.image.pure import PymagingImage
from StringIO import StringIO


@app.route('/api/encode', methods=["GET"])
def encode():
    # just a sample encoding
    data = request.args.get('data')

    print "Numbers:", data.isdigit()
    print len(data)

    img = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_H,
                      image_factory=PymagingImage)

    output = StringIO()
    img.save(output)

    with open('pic.png', 'w') as fh:
        fh.write(output.getvalue())
    output.seek(0)
    return send_file(output, mimetype='image/png')

@app.route('/api/test', methods=["GET"])
def test():
    # just a sample encoding
    data = "QR kodas bakalauriniam darbui"

    img = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_H,
                      image_factory=PymagingImage)

    output = StringIO()
    img.save(output)

    with open('pic.png', 'w') as fh:
        fh.write(output.getvalue())
    output.seek(0)
    return send_file(output, mimetype='image/png')

@app.route('/api/decode')
def decode(**kwargs):

    return jsonify(

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