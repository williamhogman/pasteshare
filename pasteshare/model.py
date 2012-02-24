import time
import pasteshare.data as data

from brukva.adisp import process,async

class Snippet(object):

    def __init__(self,_id,title,content,language,
                 creation,lastedit=None,author=0):
        
        self._id = _id
        self.title = title
        self.content  = content
        self.language = language
        self.author = author
        self.creation = creation
        if lastedit is None:
            lastedit = creation
            
        
    @staticmethod
    @async
    def _get_unused_id(callback):
        """ gets an unused id """
	cli = data.get_client()
	pcli.incr("counter:snippet",callback)


    @classmethod
    def new(cls,title,content,language,author=0):
        """ Creates a new snippet """
        creation = int(time.time())
        _id = _get_unused_id()
        return cls(_id,title,content,language,author,creation)
