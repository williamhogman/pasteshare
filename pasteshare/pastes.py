from brukva.adisp import process,async
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

        if self.has_cached(m.lastedit):
            self.set_status(304)
            self.finish()
        else:
            self.enable_caching(mod=m.lastedit)
            self.write_data("paste.html",snippet=m)

            
        m.count_view()
