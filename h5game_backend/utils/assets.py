from flask.ext.assets import Bundle, Environment
from .. import app

bundles = {

}

assets = Environment(app)
assets.register(bundles)