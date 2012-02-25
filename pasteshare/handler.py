"""
Put http handlers here
"""
import tornado.web as web
import json

_api_type = "application/vnd.pasteshare"
def _parse_mimetype(mimetype):
    if mimetype.startswith(_api_type):
        rest = mimetype[len(_api_type):]
        fmt = rest.find("+")
        if rest.startswith("."):
            version = rest[1:fmt]
        else:
            version = -1
            
        if fmt != -1:
            tp = rest[fmt+1:]
        else:
            tp = "json"

        return (version,tp)
    else:
        return False
            
    

class Handler(web.RequestHandler):
    """
    Base class for handlers in pasteshare
    """

class RESTHandler(web.RequestHandler):
    """ Base handler for REST pages """
    def parse_accept(self):
        accept = self.request.headers["Accept"]
        parsed = _parse_mimetype(accept)
        if parsed is False:
            self.api_call = False
        else:
            print(parsed)
            self.api_call = True
            self.api_version = parsed[0]
            self.api_type = parsed[1]

    def write_data(self,template=None,**data):
        """ writes or renders data depending on if this is an api call """
            
        if not self.api_call:
            if template is None:
                template = self.default_template
                
            self.render(template,**data)
            return

        def _parsed():
            for k,v in data.iteritems():
                if hasattr(v,"as_type"):
                    yield (k,v.as_type(self.api_type))
                else:
                    yield (k,v)

        data = dict(_parsed())
        
        if self.api_type is "json":
            self.write(json.dumps(data))
        self.finish()
            
        
    def prepare(self):
        self.parse_accept()
        
        
    
        
            

                
            

                
            
            

            
    
        
        

