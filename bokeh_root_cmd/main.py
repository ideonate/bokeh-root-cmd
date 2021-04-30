from argparse import ArgumentParser
import os
import logging
from bokeh import application

from bokeh.command.util import build_single_handler_application
from bokeh.server.server import Server
import click

from .readycheck import create_ready_app

import bokeh.server.views
import pathlib

INDEX_HTML = str(pathlib.Path(bokeh.server.views.__file__).parent / "app_index.html")


class BokehException(Exception):
    pass


def make_app(command, url="/", debug=False):
    # Command can be absolute, or could be relative to cwd
    cwd_original = os.getcwd()
    app_py_path = os.path.join(os.getcwd(), command)

    print("Fetching script or folder {}".format(app_py_path))

    dirname = os.path.dirname(app_py_path)

    if os.path.isdir(dirname):
        print("Changing CWD to {}".format(dirname))
        os.chdir(dirname)

    app = build_single_handler_application(app_py_path, [url])

    os.chdir(cwd_original)
    print("Changing CWD back to {}".format(cwd_original))

    return app

def get_applications(command, debug):
    apps = {}
    if len(command) == 1:
        apps = {"/": make_app(command[0], debug)}
    elif len(command) > 1:
        for cmd in command:
            application = make_app(cmd, debug)
            route = application.handlers[0].url_path()
            apps[route] = application
    return apps

def get_server_kwargs(port, ip, allow_websocket_origin, command):
    server_kwargs = {"port": port, "ip": ip}
    if allow_websocket_origin:
        server_kwargs["allow_websocket_origin"] = list(allow_websocket_origin)
    if len(command)>1:
        server_kwargs.update({"use_index": True, "redirect_root": True, "index": INDEX_HTML})
    return server_kwargs

@click.command()
@click.option("--port", default=8888, type=click.INT, help="port for the proxy server to listen on")
@click.option("--ip", default=None, help="Address to listen on")
@click.option(
    "--allow-websocket-origin", default=None, multiple=True, help="Web socket origins allowed"
)
@click.option("--debug/--no-debug", default=False, help="To display debug level logs")
@click.argument("command", nargs=-1, required=True)
def run(port, ip, debug, allow_websocket_origin, command):

    if debug:
        print("Setting debug")

    server_kwargs = get_server_kwargs(port, ip, allow_websocket_origin, command)

    applications = get_applications(command, debug)
    applications["/ready-check"] = create_ready_app()

    server = Server(applications, **server_kwargs)

    server.run_until_shutdown()


if __name__ == "__main__":

    try:

        run()

    except SystemExit as se:
        print("Caught SystemExit {}".format(se))
