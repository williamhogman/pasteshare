from brukva.adisp import process,async
import tornado.web as web

import pasteshare.handler as handler
import pasteshare.model as model



class PastesHandler(handler.RESTHandler):
    
    per_page = 20


    @web.asynchronous
    @process
    def get(self,page=0):
        start = page*self.per_page
        stop = start + self.per_page
        pastes = yield model.SnippetsCollection.get_recent_pastes(start=start,
                                                                  stop=stop)

        self.write_data("pastes.html",snippets=pastes)


    @web.asynchronous
    @process
    def post(self):
        s = model.Snippet.new(**self.data)

        # Everyone way post as anon
        if not s.anonymous:
            
            # 401 if login is required
            if not self.authenticated:
		raise web.HTTPError(401,"You need to login ppbefore as you post as you")
            # 403 posting as the wrong user is forbidden
            elif self.user.id != s.id:
		raise web.HTTPError(403,"You may not post as someone else")

                
        saved = yield s.save()

        # Created
        if saved:
            self.set_status(201)
            self.set_header("Location",self.construct_url(s.url))
            self.write_data("paste.html",snippet=s)
        else:
	     raise web.HTTPError(500,"Post failed")

        

class PasteHandler(handler.RESTHandler):
    """ Gets a paste by id"""

    @async
    @process
    def retrive(self,pid,callback):
        callback((yield model.Snippet.by_id(pid)))

    @web.asynchronous
    @process
    def head(self,pid):
        m = yield self.retrive(pid)
        
        # We can't cache responses to post because 
        self.enable_caching(mod=m.lastedit)
        self.finish()
        
    @web.asynchronous
    @process
    def get(self,pid):
        m = yield self.retrive(pid)

        if self.has_cached(m.lastedit):
            self.set_status(304)
            self.finish()
        else:
            self.enable_caching(mod=m.lastedit)
            self.write_data("paste.html",snippet=m)

            
        m.count_view()
