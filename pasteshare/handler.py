"""
Put http handlers here
"""
import time
from email.utils import parsedate
from wsgiref.handlers import format_date_time
import json

import tornado.web as web


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
            self.api_call = True
            self.api_version = parsed[0]
            self.api_type = parsed[1]


    def has_cached(self,ourmod,etag=None):
        """ Determines if the client cache is valid """
        if "If-Modified-Since" in self.request.headers:
            hdr = self.request.headers["If-Modified-Since"]
            theirmod =time.mktime(parsedate(hdr))
            return theirmod < moddate
        elif "If-None-Match" in self.request.headers and etag is not None:
            return self.request.headers["ETag"] == etag

    def enable_caching(self,cache_control="Public",mod=None,etag=None):
        if cache_control is not None:
            self.set_header("Cache-Control",cache_control)

        if mod is not None:
            self.set_header("Last-Modified",format_date_time(float(mod)))

        if etag is not None:
            self.set_header("ETag",etag)
            
        
            
    
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
        
        
    
        
            

                
            

                
            
            

            
    
        
        

