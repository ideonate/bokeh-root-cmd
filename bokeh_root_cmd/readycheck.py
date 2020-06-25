from bokeh.application import Application
from bokeh.application.handlers import Handler


class ReadyHandler(Handler):
    """
    The main Bokeh app gets upset - rejects websockets if we use that just to check if the 
    server is running. This check is made in jhsingle-native-proxy.
    So give it an extra /ready-check handler to poll for readiness.
    """
    
    def modify_document(self, doc):
        return doc

def create_ready_app():
    return Application(ReadyHandler())
