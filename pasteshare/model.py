import time

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
            
        
    @classmetod
    def _get_unused_id(cls):
        """ gets an unused id """

    @classmetod
    def new(cls,title,content,language,author=0,creation):
        """ Creates a new snippet """
        creation = int(time.time())
        return cls(_id,title,content,language,author,creation)
