from flask import Flask

app = Flask(__name__)

app.config.from_object('qr_service.settings')

app.url_map.strict_slashes = False

import qr_service.core
import qr_service.models
import qr_service.controllers
import qr_service.api

