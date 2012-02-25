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
        else:
            self.lastedit = lastedit

        self.author = author


    fields = ["title","content","language",
              "creation","lastedit","views",
              "author"]
    
    @property
    def _key(self):
        return "Snippet:{}".format(self.id)
        
    @property
    def url(self):
        return "pastes/{}".format(self.id)

    @process
    def save(self):
        if self.id == -1:
            creation  = True
            self.id = yield self._get_unused_id()
        else:
            creation = False
            
        key = self._key
        cli = data.get_client()

        pipe = cli.async.pipeline()
        
        pipe.hmset(self._key,_field_dict())
        if creation: # don't add us every save
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
        
    @process
    def count_view(self):
        """ Counts a pageview for this snippet """
        cli = data.get_client()
        yield cli.async.hincrby(self._key,"views",1)
                        
    @staticmethod
    @async
    def _get_unused_id(callback):
        """ gets an unused id """
	cli = data.get_client()
	yield cli.incr("counter:snippet",callback)


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

class SnippetsCollection(object):
    item_class = Snippet

    def __init__(self,items):
        self.items = items

    def as_type(self,datatype):
        items = list([item.as_type(datatype) for item in self.items])
        return items

    @classmethod
    @async
    @process
    def get_recent_pastes(cls,stop,start=0,callback=None):
        cli = data.get_client()
        ids = map(int,(yield cli.async.lrange("pastes",start,stop)))
        callback((yield cls.by_ids(ids)))

    @classmethod
    @async
    @process
    def by_ids(cls,ids,callback=None):
        # start up all the requests
        futures = [cls.item_class.by_id(_id) for _id in ids]
        
        out = list()

        for future in futures:
            out.append((yield future))
            
        print(out)
        callback(cls(out))
