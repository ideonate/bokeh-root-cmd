"""Test of the main functionality"""
import pytest
from bokeh.application.application import Application

from bokeh_root_cmd.main import BokehServer, PanelServer


@pytest.fixture(params=[BokehServer, PanelServer])
def server_class(request):
    return request.param

def test_get_server_kwargs_single_app(server_class):
    """Test Case: Starting one app"""
    actual = server_class._get_server_kwargs(
        port=7888,
        ip="0.0.0.0",
        allow_websocket_origin=("https://awesome-panel.org",),
        command=("test_apps/test_bokeh_hello.py",),
    )

    assert actual == {
        "port": 7888,
        "ip": "0.0.0.0",
        "allow_websocket_origin": ["https://awesome-panel.org"],
    }


def test_get_server_kwargs_multiple_apps(server_class):
    """Test Case: Starting multiple apps"""
    actual = server_class._get_server_kwargs(
        port=7888,
        ip="0.0.0.0",
        allow_websocket_origin=("https://awesome-panel.org",),
        command=("test_apps/test_bokeh_hello.py", "test_apps/test_panel_hello.py"),
    )

    assert actual == {
        "port": 7888,
        "ip": "0.0.0.0",
        "allow_websocket_origin": ["https://awesome-panel.org"],
        "use_index": True,
        "redirect_root": True,
        "index": server_class.index_html,
    }


def test_get_applications_single_app(server_class):
    """Test Case: Starting one app"""
    actual = server_class._get_applications(command=("test_apps/test_bokeh_hello.py",), debug=False)

    assert len(actual) == 1
    assert isinstance(actual["/"], Application)


def test_get_applications_multiple_apps(server_class):
    """Test Case: Starting multiple apps"""
    actual = server_class._get_applications(
        command=("test_apps/test_bokeh_hello.py", "test_apps/test_panel_hello.py"), debug=False
    )

    assert len(actual) == 2
    assert isinstance(actual["/test_bokeh_hello"], Application)
    assert isinstance(actual["/test_panel_hello"], Application)
