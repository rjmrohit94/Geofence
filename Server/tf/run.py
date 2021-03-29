import os
import argparse
from flask_cors import CORS
from flask_restful import Api

from app import app
from app.common.error import errors
from app.routes import initialize_routes


args_parser = argparse.ArgumentParser(description='Geofence')
args_parser.add_argument('--bind-ip', action='store', dest='bind_ip', type=str, default="0.0.0.0", help='Bind IP')
args_parser.add_argument('--bind-port', action='store', dest='bind_port', type=int, default=5001, help='Bind Port')
args_parser.add_argument('--config-path', action='store', dest='config_path', type=str, default=None,
                         help='Configuration file path')

args = args_parser.parse_args()

app.config["DEBUG"] = True
CORS(app)
app.config["PROPAGATE_EXCEPTIONS"] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

api = Api(app, errors=errors)
initialize_routes(api, app)

app.run(host=args.bind_ip, port=args.bind_port)
