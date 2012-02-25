import time
import pasteshare.data as data

from brukva.adisp import process,async

class Snippet(object):

    def __init__(self,title,content,language,
                 creation,lastedit=None,views=0,author=0,_id=-1):
        
        self.id = _id
        self.title = title
        self.content  = content
        self.language = language
        self.creation = creation
        self.views = views
        
        if lastedit is None:
            self.lastedit = creation

        self.author = author


    fields = ["title","content","language",
              "creation","lastedit","views",
              "author"]
    
    @property
    def _key(self):
        return "Snippet:{}".format(self.id)
        
    @process
    def save(self):
        if self.id == -1:
            self.id = yield self._get_unused_id()
        key = self._key
        cli = data.get_client()

        pipe = cli.async.pipeline()
        
        pipe.hmset(self._key,_field_dict())
        pipe.lpush("pastes",self.id) #global pastes
        pipe.lpush("user:{}:pastes".format(self.author),self.author) # user posts
        yield pipe.execute()


    def _field_dict(self):
        values = [getattr(self,field) for field in self.fields]
        return dict(zip(self.fields,values))
        
    
    def as_type(self,datatype):
        # all the fields
        data = self._field_dict()
        data.update({"id": self.id})
        return data
        
         
                        
    @staticmethod
    @async
    def _get_unused_id(callback):
        """ gets an unused id """
	cli = data.get_client()
	cli.incr("counter:snippet",callback)


    @classmethod
    @async
    @process
    def by_id(cls,_id,callback=None):
        key = "Snippet:{}".format(_id)
        cli = data.get_client()
        fields = yield cli.async.hmget(key,cls.fields)
        fields["_id"] = _id
        callback(cls(**fields))

        
    @classmethod
    def new(cls,title,content,language,author=0):
        """ Creates a new snippet """
        creation = int(time.time())
        return cls(title,content,language,author,creation)
