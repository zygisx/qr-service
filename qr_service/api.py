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


@app.route('/api/test', methods=["GET"])
def test():
    data = request.args.get('data')
    error_correction = request.args.get('errors')


    if error_correction == 'L': error_correction_code = qrcode.constants.ERROR_CORRECT_L
    elif error_correction == 'M': error_correction_code = qrcode.constants.ERROR_CORRECT_M
    elif error_correction == 'Q': error_correction_code = qrcode.constants.ERROR_CORRECT_Q
    elif error_correction == 'H': error_correction_code = qrcode.constants.ERROR_CORRECT_H
    else: error_correction_code = DEFAULT_ERROR_CORRECTION


    img = qrcode.make(data, error_correction=error_correction_code,
                      image_factory=PymagingImage)

    output = StringIO()
    img.save(output)
    output.seek(0)
    return send_file(output, mimetype='image/png')