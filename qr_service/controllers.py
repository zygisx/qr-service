import os

from flask import send_from_directory
from flask import make_response

from qr_service import app



# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
def index(**kwargs):
    return make_response(open('qr_service/templates/index.html').read())


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return make_response(open('qr_service/templates/index.html').read())



