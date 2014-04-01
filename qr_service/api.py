__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from qr_service import app
from flask.globals import request
from flask.json import jsonify
from flask.helpers import send_file
import qrcode
from qrcode.image.pure import PymagingImage
import StringIO


@app.route('/api/encode', methods=["GET"])
def encode():
    # just a sample encoding
    data = request.args.get('data')

    print "Numbers:", data.isdigit()
    print len(data)

    img = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_L,
                      image_factory=PymagingImage)

    output = StringIO.StringIO()
    img.save(output)

    with open('pic.png', 'w') as fh:
        fh.write(output.getvalue())
    output.seek(0)
    return send_file(output, mimetype='image/png')

@app.route('/api/decode')
def decode(**kwargs):

    return jsonify(

    )