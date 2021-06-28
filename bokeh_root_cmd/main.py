"""Command line wrapper to serve one or more named Bokeh scripts or folders."""
import logging
import os
import pathlib
from typing import Any, Dict, Tuple

import bokeh.server.views
import click
from bokeh.application.application import Application
from bokeh.command.util import build_single_handler_application
from bokeh.server.server import Server as _BkServer
from bokeh.server.views.root_handler import RootHandler
import logging

from .readycheck import create_ready_app

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(format=FORMAT)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

logger = logging.getLogger('bokeh_root_cmd')

class BokehServer:

    @staticmethod
    def _get_index_html():
        return str(pathlib.Path(bokeh.server.views.__file__).parent / "app_index.html")

    @staticmethod
    def _get_server_class():
        return _BkServer

    @staticmethod
    def _make_app(command: str, url: str = "/", debug: bool = False) -> Application:
        cwd_original = os.getcwd()

        # Command can be absolute, or could be relative to cwd
        app_py_path = os.path.join(os.getcwd(), command)

        if os.path.isdir(app_py_path):
            dirname = app_py_path
        else:
            dirname = os.path.dirname(app_py_path)

        if app_py_path==dirname:
            logger.debug("Fetching folder {}".format(app_py_path))
        else:
            logger.debug("Fetching script {}".format(app_py_path))

        if os.path.isdir(dirname):
            logger.debug("Changing working dir to {}".format(dirname))
            os.chdir(dirname)

        app = build_single_handler_application(app_py_path, [url])

        os.chdir(cwd_original)
        logger.debug("Changing working dir back to {}".format(cwd_original))

        return app

    @classmethod
    def _is_single_app(cls, cmd: str):
        """
        Return True if the path specified in `cmd` is exactly one app: either a single py/ipynb file 
        or a folder containing a main.py or main.ipynb file.
        """
        cmd_path = pathlib.Path(cmd)
        return cmd_path.is_file() or (cmd_path / "main.py").is_file() or (cmd_path / "main.ipynb").is_file()

    @classmethod
    def _get_applications(cls, command: Tuple[str], debug=False) -> Dict[str, Application]:
        
        if len(command) == 1 and cls._is_single_app(command[0]):
            return {"/": cls._make_app(command[0], debug)}

        apps = {}
        
        for cmd in command:
            if cls._is_single_app(cmd):
                cmds = [cmd]
            else:
                cmd_path = pathlib.Path(cmd)
                cmds = list(cmd_path.glob("*.ipynb")) + list(cmd_path.glob("*.py"))

            for singlecmd in cmds:
                application = cls._make_app(singlecmd, debug)
                route = application.handlers[0].url_path()
                apps[route] = application

        return apps

    @classmethod
    def _get_server_kwargs(cls, port, ip, allow_websocket_origin, is_single_app) -> Dict[str, Any]:
        server_kwargs = {"port": port, "ip": ip}
        if allow_websocket_origin:
            server_kwargs["allow_websocket_origin"] = list(allow_websocket_origin)
        if not is_single_app:
            server_kwargs.update(
                {"use_index": True, "redirect_root": True, "index": cls._get_index_html()}
            )
        return server_kwargs

    def run(self, port, ip, debug, allow_websocket_origin, command):
        logger.info("Starting %s", type(self).__name__)
        if debug:
            root_logger.setLevel(logging.DEBUG)

        logger.debug("ip = %s", ip)
        logger.debug("port = %s", port)
        logger.debug("debug = %s", debug)
        logger.debug("allow_websocket_origin = %s", allow_websocket_origin)
        logger.debug("command = %s", command)

        applications = self._get_applications(command, debug)
        applications["/ready-check"] = create_ready_app()
        logger.debug("applications = %s", list(applications.keys()))

        server_kwargs = self._get_server_kwargs(port, ip, allow_websocket_origin, len(applications) <= 2)
        if debug:
            server_kwargs["log_level"]="debug"
        server_kwargs["log_format"]=FORMAT
        logger.debug("server_kwargs = %s", server_kwargs)

        server = self._get_server_class()(applications, **server_kwargs)

        server.run_until_shutdown()


class PanelServer(BokehServer):

    @staticmethod
    def _get_server_class():
        from panel.io.server import Server as _PnServer

        return _PnServer

    @staticmethod
    def _get_index_html():
        from panel.io.server import INDEX_HTML as _PANEL_INDEX_HTML

        return _PANEL_INDEX_HTML


@click.command()
@click.option("--port", default=8888, type=click.INT, help="port for the proxy server to listen on")
@click.option("--ip", default=None, help="Address to listen on")
@click.option(
    "--allow-websocket-origin", default=None, multiple=True, help="Web socket origins allowed"
)
@click.option("--debug/--no-debug", default=False, help="To display debug level logs")
@click.option(
    "--server", default="bokeh", type=click.STRING, help="The server to use. One of bokeh or panel. Default is bokeh."
)
@click.argument("command", nargs=-1, required=True)
def run(port, ip, debug, allow_websocket_origin, server, command):
    if server=="panel":
        server = PanelServer()
    else:
        server = BokehServer()

    server.run(
        port=port,
        ip=ip,
        debug=debug,
        allow_websocket_origin=allow_websocket_origin,
        command=command,
    )


# Bokeh/ Panel can serve an index page with a list of applications at "/"
# The below is a workaround to avoid including the 'ready-check' application
def _root_handler_initialize_without_ready_check(self, *args, **kw):
        kw["applications"]=kw["applications"].copy()
        if "/ready-check" in kw["applications"]:
            kw["applications"].pop("/ready-check")

        self.applications = kw["applications"]
        self.prefix = kw["prefix"]
        self.index = kw["index"]
        self.use_redirect = kw["use_redirect"]

RootHandler.initialize = _root_handler_initialize_without_ready_check


if __name__ == "__main__":
    try:
        run()
    except SystemExit as se:
        logger.error("Caught SystemExit {}".format(se))
