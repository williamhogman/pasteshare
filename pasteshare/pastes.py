from brukva.adisp import process,async
from wsgiref.handlers import format_date_time
import tornado.web as web

import pasteshare.handler as handler
import pasteshare.model as model



class PastesHandler(handler.RESTHandler):

    def get(self,page=0):
        pass

class PasteHandler(handler.RESTHandler):
    """ Gets a paste by id"""

    @web.asynchronous
    @process
    def get(self,pid):
        m = yield model.Snippet.by_id(pid)
        self.set_header("Last-Modified",format_date_time(float(m.lastedit)))
        self.write_data("paste.html",snippet=m)
        
