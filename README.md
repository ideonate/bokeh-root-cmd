# bokeh-root-cmd

Command line wrapper to run one or more named Bokeh/Panel scripts/folders as root URL.

This project is used in [ContainDS Dashboards](https://github.com/ideonate/cdsdashboards), which is a user-friendly
way to launch Jupyter notebooks as shareable dashboards inside JupyterHub. Also works with Bokeh, Dash, Panel, Streamlit and other visualization frameworks.

The published PyPI/Conda packages DO NOT bring in Bokeh or Panel as explicit dependencies, so you may 
need to install those separately in your environment.

## Install and Run

Install using pip.

```bash
pip install bokeh-root-cmd
```

The file to start is specified on the command line, for example:

```bash
bokeh-root-cmd ~/Dev/mybokehscript.py
```

By default the server will listen on port 8888. To specify a different **port**, use the --port flag.

```bash
bokeh-root-cmd --port=8888 ~/Dev/mybokehscript.py
```

To use the Panel server use the --server flag.

```bash
bokeh-root-cmd --server=panel ~/Dev/mybokehscript.py
```

To run directly in python: `python -m bokeh_root_cmd.main <rest of command line>`

## Other command line args

--allow-websocket-origin

--debug

--ip

## Tests

In order to be able to test manually you would need to `pip install panel pytest`. This will also install bokeh.

### Automated Tests

```bash
pytest tests.py
```

### Single File on Bokeh Server

Run `bokeh-root-cmd test_apps/test_bokeh_hello.py` and verify the app is running at `http://localhost:8888`.

### Single File on Panel Server

Run `bokeh-root-cmd --server=panel test_apps/test_panel_hello.py` and verify the app is running at `http://localhost:8888`.

### Multiple Files on Bokeh Server

Run `bokeh-root-cmd test_apps/*.py` and verify the app index is running at `http://localhost:8888` and test apps at `http://localhost:8888/test_bokeh_hello` and `http://localhost:8888/test_panel_hello`.

### Multiple Files on Panel Server

Run `bokeh-root-cmd --server=panel test_apps/*.py` and verify the app index is running at `http://localhost:8888` and test apps at `http://localhost:8888/test_bokeh_hello` and `http://localhost:8888/test_panel_hello`. Note that no `ready-check' app is included in the index list.

You can also specify them individually

Run `bokeh-root-cmd --server=panel test_apps/test_bokeh_hello.py test_apps/test_panel_hello.py` and verify the app index is running at `http://localhost:8888` and test apps at `http://localhost:8888/test_bokeh_hello` and `http://localhost:8888/test_panel_hello`. Note that no `ready-check' app is included in the index list.


Thank you to [MarcSkovMadsen](https://github.com/MarcSkovMadsen) for contributions.

## Changelog

0.1.2 - Fix for Panel root dashboard when serving multiple apps. Previously caused problems in some browsers.
