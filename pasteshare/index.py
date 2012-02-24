import pasteshare.handler as handler


_pastes = "/pastes"


class IndexHandler(handler.RESTHandler):
    """ Handler for the index page """
    default_template = "index"
    def get(self):
        self.write_data(pastes=_pastes)
