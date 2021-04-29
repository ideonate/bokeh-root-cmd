"""We can use this to test the bokeh_root_cmd"""
import panel as pn


def test_panel_app():
    """Returns a Panel test app that has been marked `.servable()`

    Returns:
        pn.Column: A Column based Panel app
    """
    slider = pn.widgets.FloatSlider(name="Slider")
    return pn.Column("# Panel Test App", slider, slider.param.value).servable()


if __name__.startswith("bokeh"):
    test_panel_app()
