"""Command line wrapper to serve one or more named Bokeh scripts or folders."""
import logging
import os
import pathlib
from typing import Any, Dict, Tuple

import bokeh.server.views
import click
from bokeh.application.application import Application
from bokeh.command.util import build_single_handler_application
from bokeh.server.server import Server

from .readycheck import create_ready_app

class BokehServer():
    index_html = str(pathlib.Path(bokeh.server.views.__file__).parent / "app_index.html")
    server_class = Server

    @staticmethod
    def _make_app(command: str, url: str="/", debug: bool=False) -> Application:
        cwd_original = os.getcwd()

        # Command can be absolute, or could be relative to cwd
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

    @classmethod
    def _get_applications(cls, command: Tuple[str], debug=False) -> Dict[str, Application]:
        apps = {}
        if len(command) == 1:
            apps = {"/": cls._make_app(command[0], debug)}
        elif len(command) > 1:
            for cmd in command:
                application = cls._make_app(cmd, debug)
                route = application.handlers[0].url_path()
                apps[route] = application
        return apps

    @classmethod
    def _get_server_kwargs(cls, port, ip, allow_websocket_origin, command) -> Dict[str, Any]:
        server_kwargs = {"port": port, "ip": ip}
        if allow_websocket_origin:
            server_kwargs["allow_websocket_origin"] = list(allow_websocket_origin)
        if len(command)>1:
            server_kwargs.update({"use_index": True, "redirect_root": True, "index": cls.index_html})
        return server_kwargs

    def run(self, port, ip, debug, allow_websocket_origin, command):
        if debug:
            print("Setting debug")

        server_kwargs = self._get_server_kwargs(port, ip, allow_websocket_origin, command)

        applications = self._get_applications(command, debug)
        applications["/ready-check"] = create_ready_app()

        server = self.server_class(applications, **server_kwargs)

        server.run_until_shutdown()

@click.command()
@click.option("--port", default=8888, type=click.INT, help="port for the proxy server to listen on")
@click.option("--ip", default=None, help="Address to listen on")
@click.option(
    "--allow-websocket-origin", default=None, multiple=True, help="Web socket origins allowed"
)
@click.option("--debug/--no-debug", default=False, help="To display debug level logs")
# @click.option("--panel/--no-panel", default=False, help="Whether or not to serve using the Panel server")
@click.argument("command", nargs=-1, required=True)
def run(port, ip, debug, allow_websocket_origin, command):
    server = BokehServer()
    server.run(port=port, ip=ip, debug=debug, allow_websocket_origin=allow_websocket_origin, command=command)

if __name__ == "__main__":
    try:
        run()
    except SystemExit as se:
        print("Caught SystemExit {}".format(se))
