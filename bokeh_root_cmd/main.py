import os
import logging

from bokeh.command.util import build_single_handler_application
from bokeh.server.server import Server
import click

class BokehException(Exception):
    pass

def make_app(command, debug=False):

    # Command can be absolute, or could be relative to cwd
    app_py_path = os.path.join(os.getcwd(), command)

    print("Fetching Bokeh script or folder {}".format(app_py_path))

    app = build_single_handler_application(app_py_path, ['/'])

    return app


@click.command()
@click.option('--port', default=8888, type=click.INT, help='port for the proxy server to listen on')
@click.option('--ip', default=None, help='Address to listen on')
@click.option('--allow-websocket-origin', default=None, multiple=True, help='Web socket origins allowed')
@click.option('--debug/--no-debug', default=False, help='To display debug level logs')
@click.argument('command', nargs=1, required=True)
def run(port, ip, debug, allow_websocket_origin, command):

    if debug:
        print('Setting debug')

    app = make_app(command, debug)

    server_kwargs = {'port': port, 'ip': ip}

    if allow_websocket_origin:
        server_kwargs['allow_websocket_origin'] = list(allow_websocket_origin)

    server = Server({'/': app}, **server_kwargs)

    server.run_until_shutdown()

    
if __name__ == '__main__':

    try:

        run()

    except SystemExit as se:
        print('Caught SystemExit {}'.format(se))
