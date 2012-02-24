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
        if template is None:
            template = self.default_template
        if not self.api_call:
            self.render(template,**data)
        elif self.api_type is "json":
            self.write(json.dumps(data))
            
        
    def prepare(self):
        self.parse_accept()
        
        
    
        
            

                
            

                
            
            

            
    
        
        

