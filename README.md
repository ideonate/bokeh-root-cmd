# bokeh-root-cmd

Command line wrapper to run a named Bokeh script/folder as root URL.

This project is used in [ContainDS Dashboards](https://github.com/ideonate/cdsdashboards), which is a user-friendly 
way to launch Jupyter notebooks as shareable dashboards inside JupyterHub. Also works with Streamlit and other 
visualization frameworks.

## Install and Run

Install using pip.

```
pip install bokeh-root-cmd
```

The file to start is specified on the command line, for example:

```
bokeh-root-cmd ~/Dev/mybokehscript.py
```

By default the server will listen on port 8888

To specify a different port, use the --port flag.

```
bokeh-root-cmd --port=8888 ~/Dev/mybokehscript.py
```

To run directly in python: `python -m bokeh_root_cmd.main <rest of command line>`

## Other command line args

--allow-websocket-origin

--debug

--ip
