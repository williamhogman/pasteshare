import time
import pasteshare.data as data

from brukva.adisp import process,async

class Snippet(object):

    def __init__(self,title,content,language,
                 creation,views=0,lastedit=None,author=0,_id=-1):
        
        self.id = _id
        self.title = title
        self.content  = content
        self.language = language
        self.author = author
        self.creation = creation

        if lastedit is None:
            self.lastedit = creation

    @property
    def _key(self):
        return "Snippet:{}".format(self.id)
        
    @process
    def save(self):
        if self.id == -1:
            self.id = yield self._get_unused_id()
        key = self._key
        cli = data.get_client()
        
        yield cli.async.hmset(self._key,{
            "title": self.title,
            "content": self.content,
            "language": self.language,
            "author": self.author,
            "creation": self.creation
            })
                        
            
    
    @staticmethod
    @async
    def _get_unused_id(callback):
        """ gets an unused id """
	cli = data.get_client()
	cli.incr("counter:snippet",callback)


    @classmethod
    def new(cls,title,content,language,author=0):
        """ Creates a new snippet """
        creation = int(time.time())
        return cls(title,content,language,author,creation)
